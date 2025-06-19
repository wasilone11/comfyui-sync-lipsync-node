import time
import requests
from pathlib import Path
from sync import Sync
from sync.common import Audio, Video, GenerationOptions
from sync.core.api_error import ApiError


class SyncLipsyncNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "audio_url": ("STRING", {"default": ""}),
                "api_key": ("STRING", {"default": ""}),
                "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
                "model": (["lipsync-2", "lipsync-1.9.0-beta"],),
                "segment_secs": ("STRING", {"default": ""}),
                "segment_frames": ("STRING", {"default": ""}),
                "sync_mode": (["loop", "bounce", "cut_off", "silence", "remap"], {"default": "cut_off"}),
                "temperature": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0}),
                "active_speaker": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "lipsync_generate"
    CATEGORY = "Sync.so"
    OUTPUT_NODE = True

    def lipsync_generate(
        self,
        video_url,
        audio_url,
        api_key,
        poll_interval,
        model,
        segment_secs,
        segment_frames,
        sync_mode,
        temperature,
        active_speaker,
    ):
        client = Sync(base_url="https://api.sync.so", api_key=api_key).generations

        # Prepare video kwargs
        video_kwargs = {}
        if segment_secs:
            try:
                video_kwargs["segments_secs"] = eval(segment_secs)
            except Exception:
                return {
                    "ui": {"texts": []},
                    "result": ("Invalid format for segment_secs. Example: [[5.0, 10.0]]",)
                }

        if segment_frames:
            try:
                video_kwargs["segments_frames"] = eval(segment_frames)
            except Exception:
                return {
                    "ui": {"texts": []},
                    "result": ("Invalid format for segment_frames. Example: [[100, 200]]",)
                }

        try:
            response = client.create(
                input=[Video(url=video_url, **video_kwargs), Audio(url=audio_url)],
                model=model,
                options=GenerationOptions(
                    sync_mode=sync_mode,
                    temperature=temperature,
                    active_speaker=active_speaker,
                ),
            )
        except ApiError as e:
            return {
                "ui": {"texts": []},
                "result": (f"Error creating generation: {e.status_code} - {e.body}",)
            }

        job_id = response.id
        status = None
        while status not in ['COMPLETED', 'FAILED']:
            time.sleep(poll_interval)
            generation = client.get(job_id)
            status = generation.status

        if status == 'COMPLETED':
            output_url = generation.output_url
            timestamp = int(time.time())
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            output_filename = f"sync_output_{timestamp}.mp4"
            output_path = output_dir / output_filename

            try:
                r = requests.get(output_url)
                r.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(r.content)
            except Exception as e:
                return {
                    "ui": {"texts": []},
                    "result": (f"Failed to download video: {str(e)}",)
                }

            return {
                "ui": {
                    "videos": [{
                        "filename": output_filename,
                        "subfolder": "",
                        "type": "output"
                    }]
                },
                "result": (str(output_path),)
            }
        else:
            return {
                "ui": {"texts": []},
                "result": (f"Generation failed for job {job_id}",)
            }


# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "SyncLipsyncNode": SyncLipsyncNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SyncLipsyncNode": "Sync.so Lipsync Generator"
}

print("✅ Sync.so node with video preview loaded.")
