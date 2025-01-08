import os
import base64
import requests
from langchain_core.tools import tool
from .config import config
from typing import Dict, Union

image_analysis_config = config.get("analyze_image", {})

OPENAI_API_KEY = image_analysis_config.get("openai_api_key")
OPENAI_BASE_URL = image_analysis_config.get("openai_base_url", "https://api.openai.com/v1")
OPENAI_MODEL = image_analysis_config.get("model")

@tool(parse_docstring=True)
def analyze_image(query: str, image_source: str) -> Dict[str, Union[str, dict]]:
    """Analyzes an image based on a textual query, leveraging a visual model.
    
    Args:
        query: The image information to be retrieved.
        image_source: The image source, which can be an image URL (http:// or https://), a Base64 encoded image string, or a Base64 image string with the "image/" prefix.
    """

    image_download_path = image_analysis_config.get("img_folder")
    os.makedirs(image_download_path, exist_ok=True)
    base64_image = None

    try:
        if image_source.startswith(("http://", "https://")):
            try:
                if "multimedia.nt.qq.com.cn" in image_source and image_source.startswith("https"):
                    image_source = image_source.replace("https", "http", 1)

                response = requests.get(image_source, timeout=10)
                response.raise_for_status()

                file_path = os.path.join(image_download_path, "downloaded_image.jpg")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                with open(file_path, "rb") as f:
                    encoded_image = base64.b64encode(f.read()).decode("utf-8")
                base64_image = f"data:image/jpeg;base64,{encoded_image}"

            except requests.exceptions.RequestException as e:
                error_message = f"Failed to download image from URL: {e}"
                return {"status": "error", "message": error_message}

        elif image_source.startswith(("data:image/", "data:application/")):
            base64_image = image_source
        else:
            base64_image = f"data:image/jpeg;base64,{image_source}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }

        data = {
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """You are now a pair of keen eyes. Your task is to observe and understand the images uploaded by the user and, based on the user's instructions, return the required information and a detailed description of the image.

Please note the following requirements:
1. You can only output in plain text format. You cannot use any text rendering formats, such as Markdown, LaTeX, **bold**, *italics*, etc.
2. You need to extract key information from the image based on the user's instructions.
3. You need to provide a detailed description of the image, including but not limited to the overall content, colors, composition, details, etc.
4. Your description should be objective and accurate, avoiding any personal subjective assumptions.
5. Your language should be fluent, natural, and easy to understand.
6. You need to respond in the language used by the user. If the user uses Chinese, you need to respond in Chinese; if the user uses English, you need to respond in English, and so on.

After understanding the image uploaded by the user and their instructions, please begin your observation and description."""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": query,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 2048
        }

        response = requests.post(f"{OPENAI_BASE_URL}/chat/completions", headers=headers, json=data, timeout=60)
        response.raise_for_status()

        completion = response.json()
        return {"status": "success", "data": completion}

    except requests.exceptions.RequestException as e:
        error_message = f"Error communicating with OpenAI API: {e}"
        return {"status": "error", "message": error_message}
    except Exception as e:
        error_message = f"An unexpected error occurred during image analysis: {e}"
        return {"status": "error", "message": error_message}

tools = [analyze_image]

