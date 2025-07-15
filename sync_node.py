# import time
# import requests
# from pathlib import Path
# from sync import Sync
# from sync.common import Audio, Video, GenerationOptions
# from sync.core.api_error import ApiError


# class SyncLipsyncNode:
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "video_url": ("STRING", {"default": ""}),
#                 "audio_url": ("STRING", {"default": ""}),
#                 "api_key": ("STRING", {"default": ""}),
#                 "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
#                 "model": (["lipsync-2", "lipsync-1.9.0-beta"],),
#                 "segment_secs": ("STRING", {"default": ""}),
#                 "segment_frames": ("STRING", {"default": ""}),
#                 "sync_mode": (["loop", "bounce", "cut_off", "silence", "remap"], {"default": "cut_off"}),
#                 "temperature": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0}),
#                 "active_speaker": ("BOOLEAN", {"default": False}),
#             }
#         }

#     RETURN_TYPES = ("STRING",)
#     RETURN_NAMES = ("output_path",)
#     FUNCTION = "lipsync_generate"
#     CATEGORY = "Sync.so"
#     OUTPUT_NODE = True

#     def lipsync_generate(
#         self,
#         video_url,
#         audio_url,
#         api_key,
#         poll_interval,
#         model,
#         segment_secs,
#         segment_frames,
#         sync_mode,
#         temperature,
#         active_speaker,
#     ):
#         client = Sync(base_url="https://api.sync.so", api_key=api_key).generations

#         # Prepare video kwargs
#         video_kwargs = {}
#         if segment_secs:
#             try:
#                 video_kwargs["segments_secs"] = eval(segment_secs)
#             except Exception:
#                 return {
#                     "ui": {"texts": []},
#                     "result": ("Invalid format for segment_secs. Example: [[5.0, 10.0]]",)
#                 }

#         if segment_frames:
#             try:
#                 video_kwargs["segments_frames"] = eval(segment_frames)
#             except Exception:
#                 return {
#                     "ui": {"texts": []},
#                     "result": ("Invalid format for segment_frames. Example: [[100, 200]]",)
#                 }

#         try:
#             response = client.create(
#                 input=[Video(url=video_url, **video_kwargs), Audio(url=audio_url)],
#                 model=model,
#                 options=GenerationOptions(
#                     sync_mode=sync_mode,
#                     temperature=temperature,
#                     active_speaker=active_speaker,
#                 ),
#             )
#         except ApiError as e:
#             return {
#                 "ui": {"texts": []},
#                 "result": (f"Error creating generation: {e.status_code} - {e.body}",)
#             }

#         job_id = response.id
#         status = None
#         while status not in ['COMPLETED', 'FAILED']:
#             time.sleep(poll_interval)
#             generation = client.get(job_id)
#             status = generation.status

#         if status == 'COMPLETED':
#             output_url = generation.output_url
#             timestamp = int(time.time())
#             output_dir = Path("output")
#             output_dir.mkdir(exist_ok=True)
#             output_filename = f"sync_output_{timestamp}.mp4"
#             output_path = output_dir / output_filename

#             try:
#                 r = requests.get(output_url)
#                 r.raise_for_status()
#                 with open(output_path, "wb") as f:
#                     f.write(r.content)
#             except Exception as e:
#                 return {
#                     "ui": {"texts": []},
#                     "result": (f"Failed to download video: {str(e)}",)
#                 }

#             return {
#                 "ui": {
#                     "videos": [{
#                         "filename": output_filename,
#                         "subfolder": "",
#                         "type": "output"
#                     }]
#                 },
#                 "result": (str(output_path),)
#             }
#         else:
#             return {
#                 "ui": {"texts": []},
#                 "result": (f"Generation failed for job {job_id}",)
#             }


# # Node registration for ComfyUI
# NODE_CLASS_MAPPINGS = {
#     "SyncLipsyncNode": SyncLipsyncNode,
# }

# NODE_DISPLAY_NAME_MAPPINGS = {
#     "SyncLipsyncNode": "Sync.so Lipsync Generator"
# }

# print("✅ Sync.so node with video preview loaded.")

import time, requests
from pathlib import Path
from os.path import getsize
from sync import Sync
from sync.common import Audio, Video, GenerationOptions


# ────────── INPUT NODE
class SyncLipsyncInputNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default": ""}),
                "audio_path": ("STRING", {"default": ""}),
                "video_url":  ("STRING", {"default": ""}),
                "audio_url":  ("STRING", {"default": ""}),
                "api_key":    ("STRING", {"default": ""}),
                "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
            }
        }

    RETURN_TYPES = ("SYNC_INPUT",)
    RETURN_NAMES = ("sync_input",)
    FUNCTION = "provide"
    CATEGORY = "Sync.so/Lipsync"

    def provide(self, video_path, audio_path, video_url, audio_url, api_key, poll_interval):
        return ({
            "video_path": video_path,
            "audio_path": audio_path,
            "video_url": video_url,
            "audio_url": audio_url,
            "api_key": api_key,
            "poll_interval": poll_interval,
        },)


# ────────── GENERATE NODE
class SyncLipsyncMainNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sync_input": ("SYNC_INPUT", {}),
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
    CATEGORY = "Sync.so/Lipsync"

    def lipsync_generate(self, sync_input, model, segment_secs, segment_frames, sync_mode, temperature, active_speaker):
        video_path = sync_input["video_path"]
        audio_path = sync_input["audio_path"]
        video_url = sync_input["video_url"]
        audio_url = sync_input["audio_url"]
        api_key = sync_input["api_key"]
        poll_interval = sync_input["poll_interval"]

        print(" lipsync_generate called")

        MAX_BYTES = 20 * 1024 * 1024
        headers = {"x-api-key": api_key}

        try:
            if (video_path and Path(video_path).exists() and getsize(video_path) <= MAX_BYTES) or \
               (audio_path and Path(audio_path).exists() and getsize(audio_path) <= MAX_BYTES):
                print(" Using file upload (v2)")
                url = "https://api.sync.so/v2/generate"
                data = {
                    "model": model,
                    "sync_mode": sync_mode,
                    "temperature": str(temperature),
                    "active_speaker": str(active_speaker).lower(),
                }

                if segment_secs:
                    data["segments_secs"] = segment_secs
                if segment_frames:
                    data["segments_frames"] = segment_frames

                files = {}
                if video_path and Path(video_path).exists():
                    files["video"] = open(video_path, "rb")
                    print(f" Opening video file: {video_path}")
                elif video_url:
                    data["video_url"] = video_url
                    print(f" Using video URL: {video_url}")

                if audio_path and Path(audio_path).exists():
                    files["audio"] = open(audio_path, "rb")
                    print(f" Opening audio file: {audio_path}")
                elif audio_url:
                    data["audio_url"] = audio_url
                    print(f" Using audio URL: {audio_url}")

                print(" Sending POST request...")
                res = requests.post(url, headers=headers, files=files or None, data=data)
                print(f" Response code: {res.status_code}")
                res.raise_for_status()
                job_id = res.json()["id"]
                print(f" Job ID: {job_id}")
            else:
                print(" Using SDK fallback")
                client = Sync(base_url="https://api.sync.so", api_key=api_key).generations
                video_kwargs = {}
                if segment_secs:
                    video_kwargs["segments_secs"] = eval(segment_secs)
                if segment_frames:
                    video_kwargs["segments_frames"] = eval(segment_frames)

                response = client.create(
                    input=[Video(url=video_url, **video_kwargs), Audio(url=audio_url)],
                    model=model,
                    options=GenerationOptions(
                        sync_mode=sync_mode,
                        temperature=temperature,
                        active_speaker=active_speaker,
                    ),
                )
                job_id = response.id

            # Polling
            status_url = f"https://api.sync.so/v2/generate/{job_id}"
            print(f" Polling job: {job_id}")
            status = None

            while status not in ["COMPLETED", "FAILED"]:
                print(f" Waiting {poll_interval}s...")
                time.sleep(poll_interval)
                poll = requests.get(status_url, headers=headers)
                poll.raise_for_status()
                status = poll.json().get("status")
                print(f" Job status: {status}")

            if status != "COMPLETED":
                print(f" Job failed")
                return ("",)

            output_url = poll.json().get("outputUrl") or (poll.json().get("result") or {}).get("outputUrl")
            print(f" Downloading video from: {output_url}")
            timestamp = int(time.time())
            output_path = Path("output") / f"sync_output_{timestamp}.mp4"
            Path("output").mkdir(exist_ok=True)

            r = requests.get(output_url)
            r.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(r.content)
            print(f" Video saved to: {output_path}")
            return (str(output_path),)

        except Exception as e:
            print(f"🔥 Exception: {e}")
            return ("",)


# ────────── OUTPUT NODE
class SyncLipsyncOutputNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"output_path": ("STRING", {})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "passthrough"
    CATEGORY = "Sync.so/Lipsync"
    OUTPUT_NODE = True

    def passthrough(self, output_path):
        if not output_path or not Path(output_path).exists():
            return {
                "ui": {"texts": [" No video output was generated."]},
                "result": (output_path,)
            }

        return {
            "ui": {
                "videos": [{
                    "filename": Path(output_path).name,
                    "subfolder": "",
                    "type": "output"
                }]
            },
            "result": (output_path,)
        }


# ────────── REGISTER
NODE_CLASS_MAPPINGS = {
    "SyncLipsyncInputNode": SyncLipsyncInputNode,
    "SyncLipsyncMainNode": SyncLipsyncMainNode,
    "SyncLipsyncOutputNode": SyncLipsyncOutputNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SyncLipsyncInputNode": "Sync.so Lipsync – Input",
    "SyncLipsyncMainNode": "Sync.so Lipsync – Generate",
    "SyncLipsyncOutputNode": "Sync.so Lipsync – Output",
}

print("Sync.so hybrid upload module loaded.")
