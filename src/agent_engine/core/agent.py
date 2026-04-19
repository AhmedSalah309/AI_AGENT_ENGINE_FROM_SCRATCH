import json
from typing import Optional, Iterator, Any

import requests

from agent_engine.config.logger import logger
from agent_engine.config.settings import settings


class Agent:
    def __init__(
        self, name: str = "A-EIL Core Agent", system_prompt: Optional[str] = None
    ):
        self.name = name
        self.system_prompt = system_prompt or "You are a helpful AI assistant."

    def generate_stream(self, conversation: Any) -> Iterator[str]:
        messages_payload = []

        if self.system_prompt:
            messages_payload.append({"role": "system", "content": self.system_prompt})

        # Use all messages, as the Conversation class manages the context
        recent_messages = conversation.messages

        for msg in recent_messages:
            if msg.content and msg.role in ["user", "assistant"]:
                messages_payload.append(
                    {"role": msg.role, "content": msg.content.strip()}
                )

        payload = {
            "model": settings.DEFAULT_MODEL,
            "messages": messages_payload,
            "stream": True,
            "options": {
                "temperature": 0.7,
                "num_predict": 512,
                "top_p": 0.9,
            },
        }

        try:
            response = requests.post(
                settings.OLLAMA_BASE_URL, json=payload, stream=True, timeout=60
            )
            response.raise_for_status()

            # Use iter_lines to read the full JSON in each iteration
            # This solves the multi-byte characters issue like Arabic and Chinese
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))

                        if data.get("done", False):
                            break

                        content = data.get("message", {}).get("content", "")
                        if content:
                            yield content
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue

        except requests.exceptions.Timeout:
            error_msg = "Request timeout. Try again."
            logger.error(error_msg)
            yield error_msg
        except requests.exceptions.ConnectionError:
            error_msg = "Cannot connect to Ollama."
            logger.error(error_msg)
            yield error_msg
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(error_msg)
            yield error_msg
