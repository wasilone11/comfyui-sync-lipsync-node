# import time
# from pathlib import Path
# from sync import Sync
# from sync.common import Audio, Video, GenerationOptions
# from sync.core.api_error import ApiError

# class SyncLipsyncNode:
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "video_url": ("STRING", {"default": "https://assets.sync.so/docs/example-video.mp4"}),
#                 "audio_url": ("STRING", {"default": "https://assets.sync.so/docs/example-audio.wav"}),
#                 "api_key": ("STRING", {"default": ""}),
#                 "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
#             }
#         }

#     RETURN_TYPES = ("STRING",)
#     RETURN_NAMES = ("output_url",)
#     FUNCTION = "lipsync_generate"
#     CATEGORY = "Sync.so"
#     OUTPUT_NODE = True  # ✅ This makes it an output node
    
#     def lipsync_generate(self, video_url, audio_url, api_key, poll_interval):
#         client = Sync(base_url="https://api.sync.so", api_key=api_key).generations

#         try:
#             response = client.create(
#                 input=[Video(url=video_url), Audio(url=audio_url)],
#                 model="lipsync-2",
#                 options=GenerationOptions(sync_mode="cut_off"),
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
#             filename = f"sync_lipsync_output_{int(time.time())}.txt"
#             output_dir = Path("output")
#             output_dir.mkdir(exist_ok=True)
#             output_path = output_dir / filename

#             with open(output_path, "w") as f:
#                 f.write(output_url)

#             return {
#                 "ui": {
#                     "texts": [{
#                         "filename": filename,
#                         "subfolder": "",
#                         "type": "output"
#                     }]
#                 },
#                 "result": (output_url,)
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




#-----------------------------------------------------------------------------------------------
#Save the video

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
#                 "video_url": ("STRING", {"default": "https://assets.sync.so/docs/example-video.mp4"}),
#                 "audio_url": ("STRING", {"default": "https://assets.sync.so/docs/example-audio.wav"}),
#                 "api_key": ("STRING", {"default": ""}),
#                 "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
#             }
#         }

#     RETURN_TYPES = ("STRING",)
#     RETURN_NAMES = ("output_path",)
#     FUNCTION = "lipsync_generate"
#     CATEGORY = "Sync.so"
#     OUTPUT_NODE = True

#     def lipsync_generate(self, video_url, audio_url, api_key, poll_interval):
#         client = Sync(base_url="https://api.sync.so", api_key=api_key).generations

#         try:
#             response = client.create(
#                 input=[Video(url=video_url), Audio(url=audio_url)],
#                 model="lipsync-2",
#                 options=GenerationOptions(sync_mode="cut_off"),
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

# With multiple model support

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
#                 "video_url": ("STRING", {"default": "https://assets.sync.so/docs/example-video.mp4"}),
#                 "audio_url": ("STRING", {"default": "https://assets.sync.so/docs/example-audio.wav"}),
#                 "api_key": ("STRING", {"default": ""}),
#                 "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
#                 "model": (["lipsync-2", "lipsync-1.9.0-beta"],),
#             }
#         }

#     RETURN_TYPES = ("STRING",)
#     RETURN_NAMES = ("output_path",)
#     FUNCTION = "lipsync_generate"
#     CATEGORY = "Sync.so"
#     OUTPUT_NODE = True

#     def lipsync_generate(self, video_url, audio_url, api_key, poll_interval, model):
#         client = Sync(base_url="https://api.sync.so", api_key=api_key).generations

#         try:
#             response = client.create(
#                 input=[Video(url=video_url), Audio(url=audio_url)],
#                 model=model,
#                 options=GenerationOptions(sync_mode="cut_off"),
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
#                 "video_url": ("STRING", {"default": "https://assets.sync.so/docs/example-video.mp4"}),
#                 "audio_url": ("STRING", {"default": "https://assets.sync.so/docs/example-audio.wav"}),
#                 "api_key": ("STRING", {"default": ""}),
#                 "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
#                 "model": (["lipsync-2", "lipsync-1.9.0-beta"],),
#                 "segment_secs": ("STRING", {"default": ""}),
#                 "segment_frames": ("STRING", {"default": ""}),
#             }
#         }

#     RETURN_TYPES = ("STRING",)
#     RETURN_NAMES = ("output_path",)
#     FUNCTION = "lipsync_generate"
#     CATEGORY = "Sync.so"
#     OUTPUT_NODE = True

#     def lipsync_generate(self, video_url, audio_url, api_key, poll_interval, model, segment_secs, segment_frames):
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
#                 options=GenerationOptions(sync_mode="cut_off"),
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




# IS this the END!!!! Filhaal ye acha hai



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
                "video_url": ("STRING", {"default": "https://assets.sync.so/docs/example-video.mp4"}),
                "audio_url": ("STRING", {"default": "https://assets.sync.so/docs/example-audio.wav"}),
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

###ENDDDDDD

# import time
# import json
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
#                 "video_url": ("STRING", {"default": "https://assets.sync.so/docs/example-video.mp4"}),
#                 "audio_url": ("STRING", {"default": ""}),  # optional if TTS used
#                 "tts_text": ("STRING", {"default": ""}),  # text for TTS
#                 "tts_provider": ("STRING", {"default": ""}),  # JSON string for TTS provider config
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
#         tts_text,
#         tts_provider,
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

#         # Prepare inputs: video + (audio or TTS)
#         inputs = [Video(url=video_url, **video_kwargs)]

#         if tts_text.strip():
#             # Use TTS input
#             try:
#                 provider_config = json.loads(tts_provider) if tts_provider else {}
#             except Exception as e:
#                 return {
#                     "ui": {"texts": []},
#                     "result": (f"Invalid JSON format for tts_provider: {str(e)}",)
#                 }
#             inputs.append(
#                 {
#                     "type": "text",
#                     "provider": provider_config
#                 }
#             )
#             # Note: Sync SDK might require a special class or raw dict. Using dict as per spec.
#         elif audio_url.strip():
#             # Use audio URL input
#             inputs.append(Audio(url=audio_url))
#         else:
#             return {
#                 "ui": {"texts": []},
#                 "result": ("Either audio_url or tts_text with tts_provider must be provided.",)
#             }

#         try:
#             response = client.create(
#                 input=inputs,
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

















#---------------------------------------------------------------------------------------------------------------------------

# import time
# from pathlib import Path
# from sync import Sync
# from sync.common import Audio, Video, GenerationOptions
# from sync.core.api_error import ApiError

# class SyncLipsyncNode:
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "video": ("VIDEO",),
#                 "audio": ("AUDIO",),
#                 "api_key": ("STRING", {"default": ""}),
#                 "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
#             }
#         }

#     RETURN_TYPES = ("STRING",)
#     RETURN_NAMES = ("output_url",)
#     FUNCTION = "lipsync_generate"
#     CATEGORY = "Sync.so"
#     OUTPUT_NODE = True

#     def lipsync_generate(self, video, audio, api_key, poll_interval):
#         # Extract file paths from VIDEO/AUDIO objects
#         # video_path = Path(video["filepath"]).resolve().as_uri()
#         # audio_path = Path(audio["filepath"]).resolve().as_uri()
#         video_path = Path(video["path"]).resolve().as_uri()
#         audio_path = Path(audio["path"]).resolve().as_uri()



#         client = Sync(base_url="https://api.sync.so", api_key=api_key).generations

#         try:
#             response = client.create(
#                 input=[Video(url=video_path), Audio(url=audio_path)],
#                 model="lipsync-2",
#                 options=GenerationOptions(sync_mode="cut_off"),
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
#             filename = f"sync_lipsync_output_{int(time.time())}.txt"
#             output_dir = Path("output")
#             output_dir.mkdir(exist_ok=True)
#             output_path = output_dir / filename

#             with open(output_path, "w") as f:
#                 f.write(output_url)

#             return {
#                 "ui": {
#                     "texts": [{
#                         "filename": filename,
#                         "subfolder": "",
#                         "type": "output"
#                     }]
#                 },
#                 "result": (output_url,)
#             }
#         else:
#             return {
#                 "ui": {"texts": []},
#                 "result": (f"Generation failed for job {job_id}",)
#             }

# # Register the node
# NODE_CLASS_MAPPINGS = {
#     "SyncLipsyncNode": SyncLipsyncNode,
# }

# NODE_DISPLAY_NAME_MAPPINGS = {
#     "SyncLipsyncNode": "Sync.so Lipsync Generator"
# }
# import time
# from pathlib import Path
# from sync import Sync
# from sync.common import Audio, Video, GenerationOptions
# from sync.core.api_error import ApiError

# import soundfile as sf
# import torch
# import tempfile

# class SyncLipsyncNode:
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "video": ("VIDEO",),
#                 "audio": ("AUDIO",),
#                 "api_key": ("STRING", {"default": ""}),
#                 "poll_interval": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0}),
#             }
#         }

#     RETURN_TYPES = ("STRING",)
#     RETURN_NAMES = ("output_url",)
#     FUNCTION = "lipsync_generate"
#     CATEGORY = "Sync.so"
#     OUTPUT_NODE = True

#     def save_audio_to_file(self, audio_dict):
#         waveform = audio_dict["waveform"]
#         sample_rate = audio_dict["sample_rate"]

#         # Convert tensor to numpy array with shape (samples, channels)
#         if isinstance(waveform, torch.Tensor):
#             waveform = waveform.squeeze().permute(1, 0).cpu().numpy()
#         else:
#             waveform = waveform.T  # Just in case it's numpy already

#         # Save to temporary WAV file
#         tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
#         sf.write(tmp_file.name, waveform, sample_rate)
#         tmp_file.close()
#         return tmp_file.name

#     def lipsync_generate(self, video, audio, api_key, poll_interval):
#         # Extract video path from VideoFromFile object (private attribute)
#         video_path_str = getattr(video, "_VideoFromFile__file", None)
#         if not video_path_str:
#             raise RuntimeError("Video path not found")

#         video_path = Path(video_path_str).resolve().as_uri()

#         # Save audio waveform dict to WAV file and get path
#         audio_file_path = self.save_audio_to_file(audio)
#         audio_path = Path(audio_file_path).resolve().as_uri()

#         client = Sync(base_url="https://api.sync.so", api_key=api_key).generations

#         try:
#             response = client.create(
#                 input=[Video(url=video_path), Audio(url=audio_path)],
#                 model="lipsync-2",
#                 options=GenerationOptions(sync_mode="cut_off"),
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
#             filename = f"sync_lipsync_output_{int(time.time())}.txt"
#             output_dir = Path("output")
#             output_dir.mkdir(exist_ok=True)
#             output_path = output_dir / filename

#             with open(output_path, "w") as f:
#                 f.write(output_url)

#             return {
#                 "ui": {
#                     "texts": [{
#                         "filename": filename,
#                         "subfolder": "",
#                         "type": "output"
#                     }]
#                 },
#                 "result": (output_url,)
#             }
#         else:
#             return {
#                 "ui": {"texts": []},
#                 "result": (f"Generation failed for job {job_id}",)
#             }

# # Register the node
# NODE_CLASS_MAPPINGS = {
#     "SyncLipsyncNode": SyncLipsyncNode,
# }

# NODE_DISPLAY_NAME_MAPPINGS = {
#     "SyncLipsyncNode": "Sync.so Lipsync Generator"
# }
