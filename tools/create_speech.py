import requests
from pathlib import Path
from .config import config
from langchain_core.tools import tool
from typing import Dict
import uuid
from datetime import datetime

SPEECH_CONFIG = config.get("create_speech", {})
VOICE_MAPPING: Dict[str, str] = SPEECH_CONFIG.get("voice_mapping", {})
API_KEY: str = SPEECH_CONFIG.get("siliconflow_key")
BASE_URL: str = "https://api.siliconflow.cn/v1/audio/speech"
MODEL_NAME: str = "fishaudio/fish-speech-1.5"
MAX_TEXT_LENGTH: int = SPEECH_CONFIG.get("max_text_length", 500)
ROOT_PATH: Path = Path(__file__).resolve().parents[1]
TEMP_SERVER_DIR: Path = ROOT_PATH / "temp_server" / "speech"
TEMP_SERVER_DIR.mkdir(parents=True, exist_ok=True)

def generate_filename() -> str:
    """生成基于时间戳和UUID的文件名"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8] 
    return f"{timestamp}_{unique_id}.wav"

class SiliconFlowTTS:
    """Silicon Flow TTS 服务封装"""
    def __init__(self):
        self.api_key = API_KEY
        self.voice_mapping = VOICE_MAPPING
        
    def generate_speech(self, text: str, timbre: str, output_path: Path) -> None:
        payload = {
            "model": MODEL_NAME,
            "input": text,
            "voice": self.voice_mapping.get(timbre, self.voice_mapping["xigewen"]),
            "response_format": "wav"
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        with open(output_path, 'wb') as file:
            file.write(response.content)

@tool(parse_docstring=True)
def create_speech(text: str, timbre: str = None) -> str:
    """TTS speech generation
    
    Args:
        text: Text to be converted
        timbre: timbre
    """
    if len(text) > MAX_TEXT_LENGTH:
        return f"错误: 文本超出{MAX_TEXT_LENGTH}字限制。当前长度：{len(text)}字"
        
    if not timbre or timbre not in VOICE_MAPPING:
        timbre = next(iter(VOICE_MAPPING.keys()))

    try:
        filename = generate_filename()
        output_path = TEMP_SERVER_DIR / filename
        
        tts = SiliconFlowTTS()
        tts.generate_speech(text, timbre, output_path)
        
        return f"file://{TEMP_SERVER_DIR}/{filename}"
    except Exception as e:
        return f"错误: 语音生成失败 - {str(e)}"

tools = [create_speech]
