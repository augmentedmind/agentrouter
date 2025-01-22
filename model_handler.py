import json
from litellm.integrations.custom_logger import CustomLogger
from litellm.proxy.proxy_server import UserAPIKeyAuth, DualCache
from typing import Optional, Literal

class ModelHandler(CustomLogger):
    def __init__(self):
        pass

    async def async_pre_call_hook(self, user_api_key_dict: UserAPIKeyAuth, cache: DualCache, data: dict, call_type: Literal[
            "completion",
            "text_completion",
            "embeddings",
            "image_generation",
            "moderation",
            "audio_transcription",
        ]):
        print(f"Pre call hook")
        print(f"Model: {data['model']}")

        if "metadata" in data:
            print(f"Metadata: {json.dumps(data['metadata'], indent=2)}")
        if "litellm_metadata" in data:
            print(f"LiteLLM Metadata: {json.dumps(data['litellm_metadata'], indent=2)}")
        if "extra_headers" in data:
            print(f"extra_headers: {json.dumps(data['extra_headers'], indent=2)}")
        if "proxy_server_request" in data:
            print(f"proxy_server_request: {json.dumps(data['proxy_server_request'], indent=2)}")
        print(f"Keys: {data.keys()}")
        
        # Modify the model
        data["model"] = "claude-3-5-sonnet-20241022"
        return data

model_handler_instance = ModelHandler()
