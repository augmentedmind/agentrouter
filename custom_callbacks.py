import json
from datetime import datetime
from pathlib import Path

from litellm.integrations.custom_logger import CustomLogger
import litellm
from litellm.proxy.proxy_server import UserAPIKeyAuth, DualCache
from typing import Optional, Literal

def save_debug_data(data: dict, prefix: str):
    """Save debug data to a file in .debug directory with datetime prefix"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{timestamp}_{prefix}.json"
    filepath = Path(".debug") / filename
    
    filepath.parent.mkdir(exist_ok=True)
    filepath.write_text(json.dumps(data, indent=2, default=str))

# This file includes the custom callbacks for LiteLLM Proxy
# Once defined, these can be passed in proxy_config.yaml
class MyCustomHandler(CustomLogger): # https://docs.litellm.ai/docs/observability/custom_callback#callback-class
    def __init__(self):
        pass

    #### Standard Logging Methods ####
    def log_pre_api_call(self, model, messages, kwargs): 
        debug_data = {
            "type": "pre_api_call",
            "model": model,
            "messages": messages,
            "kwargs": kwargs
        }
        save_debug_data(debug_data, "pre_api_call")

    def log_post_api_call(self, kwargs, response_obj, start_time, end_time): 
        debug_data = {
            "type": "post_api_call",
            "kwargs": kwargs,
            "response": response_obj.dict() if hasattr(response_obj, 'dict') else str(response_obj),
            "duration": (end_time - start_time).total_seconds() if (end_time and start_time) else None
        }
        save_debug_data(debug_data, "post_api_call")

    def log_stream_event(self, kwargs, response_obj, start_time, end_time):
        debug_data = {
            "type": "stream_event",
            "kwargs": kwargs,
            "response": str(response_obj),
            "duration": (end_time - start_time).total_seconds() if (end_time and start_time) else None
        }
        save_debug_data(debug_data, "stream_event")
        
    def log_success_event(self, kwargs, response_obj, start_time, end_time): 
        debug_data = {
            "type": "success_event",
            "kwargs": kwargs,
            "response": response_obj.dict() if hasattr(response_obj, 'dict') else str(response_obj),
            "duration": (end_time - start_time).total_seconds() if (end_time and start_time) else None
        }
        save_debug_data(debug_data, "success_event")

    def log_failure_event(self, kwargs, response_obj, start_time, end_time): 
        debug_data = {
            "type": "failure_event",
            "kwargs": kwargs,
            "error": str(response_obj),
            "duration": (end_time - start_time).total_seconds() if (end_time and start_time) else None
        }
        save_debug_data(debug_data, "failure_event")

    #### Async Logging Methods ####
    async def async_log_stream_event(self, kwargs, response_obj, start_time, end_time):
        debug_data = {
            "type": "async_stream_event",
            "kwargs": kwargs,
            "response": str(response_obj),
            "duration": (end_time - start_time).total_seconds() if (end_time and start_time) else None
        }
        save_debug_data(debug_data, "async_stream_event")

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        debug_data = {
            "type": "async_success_event",
            "kwargs": kwargs,
            "response": response_obj.dict() if hasattr(response_obj, 'dict') else str(response_obj),
            "duration": (end_time - start_time).total_seconds() if (end_time and start_time) else None
        }
        save_debug_data(debug_data, "async_success_event")

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        debug_data = {
            "type": "async_failure_event",
            "kwargs": kwargs,
            "error": str(response_obj),
            "duration": (end_time - start_time).total_seconds() if (end_time and start_time) else None
        }
        save_debug_data(debug_data, "async_failure_event")

    #### CALL HOOKS - proxy only #### 

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

        # Save request data
        debug_data = {
            "type": "request",
            "call_type": call_type,
            "data": data,
            "user_api_key_dict": user_api_key_dict.dict() if user_api_key_dict else None
        }
        save_debug_data(debug_data, "request")

        if "metadata" in data:
            print(f"Metadata: {json.dumps(data['metadata'], indent=2)}")
        if "litellm_metadata" in data:
            print(f"LiteLLM Metadata: {json.dumps(data['litellm_metadata'], indent=2)}")
        if "extra_headers" in data:
            print(f"extra_headers: {json.dumps(data['extra_headers'], indent=2)}")
        if "proxy_server_request" in data:
            print(f"proxy_server_request: {json.dumps(data['proxy_server_request'], indent=2)}")
        print(f"Keys: {data.keys()}")
        data["model"] = "claude-3-5-sonnet-20241022"
        return data

    async def async_post_call_failure_hook(
        self, 
        request_data: dict,
        original_exception: Exception, 
        user_api_key_dict: UserAPIKeyAuth
    ):
        # Save failure data
        debug_data = {
            "type": "response_failure",
            "request_data": request_data,
            "error": str(original_exception),
            "error_type": type(original_exception).__name__,
            "user_api_key_dict": user_api_key_dict.dict() if user_api_key_dict else None
        }
        save_debug_data(debug_data, "response_failure")

    async def async_post_call_success_hook(
        self,
        data: dict,
        user_api_key_dict: UserAPIKeyAuth,
        response,
    ):
        # Save response data
        debug_data = {
            "type": "response_success",
            "data": data,
            "response": response.dict() if hasattr(response, 'dict') else str(response),
            "user_api_key_dict": user_api_key_dict.dict() if user_api_key_dict else None
        }
        save_debug_data(debug_data, "response_success")

    async def async_moderation_hook( # call made in parallel to llm api call
        self,
        data: dict,
        user_api_key_dict: UserAPIKeyAuth,
        call_type: Literal["completion", "embeddings", "image_generation", "moderation", "audio_transcription"],
    ):
        pass

    async def async_post_call_streaming_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        response: str,
    ):
        # Save streaming response data
        debug_data = {
            "type": "response_streaming",
            "response": response,
            "user_api_key_dict": user_api_key_dict.dict() if user_api_key_dict else None
        }
        save_debug_data(debug_data, "response_streaming")

proxy_handler_instance = MyCustomHandler()
