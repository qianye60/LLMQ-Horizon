import requests
import json
import time
from pathlib import Path
from datetime import datetime
import os
from .config import config
from .prompt.prompt import prompt_all
from langchain_core.tools import tool

# 获取项目根目录
root_path = Path(__file__).resolve().parents[1]
temp_server_dir = root_path / "temp_server" / "videos"
temp_server_dir.mkdir(parents=True, exist_ok=True)

# 从配置中获取视频生成相关的配置
create_video_config = config.get("create_video", {})
siliconflow_key = create_video_config.get("siliconflow_key")
openai_base_url = create_video_config.get("openai_base_url")
openai_api_key = create_video_config.get("openai_api_key")
openai_model = create_video_config.get("model")
print(openai_model)
print(openai_api_key)

def _optimize_prompt(prompt: str) -> str:
    """优化视频提示词"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {create_video_config.get("openai_api_key")}"
    }
    
    payload = {
        "model": openai_model,
        "messages": [
            {
                "role": "system",
                "content": prompt_all.get("create_video")
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{openai_base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        if result.get("choices") and len(result["choices"]) > 0:
            optimized_prompt = result["choices"][0]["message"]["content"].strip()
            print(f"优化后的提示词: [{optimized_prompt}]")
            return optimized_prompt
        return prompt
    except Exception as e:
        print(f"提示词优化失败: {str(e)}")
        return prompt

def _submit_video_request(prompt: str, model: str = "Lightricks/LTX-Video") -> str:
    """提交视频生成请求"""
    url = "https://api.siliconflow.cn/v1/video/submit"
    headers = {
        "Authorization": f"Bearer {siliconflow_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "prompt": prompt
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("requestId")
    except Exception as e:
        print(f"提交视频请求失败: {e}")
        return None

def _get_video_status(request_id: str) -> dict:
    """获取视频生成状态"""
    url = "https://api.siliconflow.cn/v1/video/status"
    headers = {
        "Authorization": f"Bearer {siliconflow_key}",
        "Content-Type": "application/json",
    }
    data = {"requestId": request_id}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取视频状态失败: {e}")
        return None

def _save_video(url: str) -> str:
    """下载并保存视频"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        save_path = temp_server_dir / filename
        
        save_path.write_bytes(response.content)
        print(f"视频已保存到: {save_path}")
        
        return f"file://{save_path}"
    except Exception as e:
        print(f"保存视频失败: {e}")
        return None

def _get_video_url(request_id: str, max_retries: int = 10, interval: int = 5) -> str:
    """轮询获取视频URL"""
    retries = 0
    while retries < max_retries:
        status_response = _get_video_status(request_id)
        if status_response and status_response.get("status") == "Succeed":
            videos = status_response.get("results", {}).get("videos", [])
            if videos and videos[0].get("url"):
                video_url = videos[0].get("url")
                return _save_video(video_url)
        
        if status_response and status_response.get("status") == "Failed":
            print(f"视频生成失败: {status_response.get('reason', '未知原因')}")
            return None
        
        retries += 1
        print(f"等待视频生成，第 {retries} 次检查...")
        time.sleep(interval)
    
    return None

@tool(parse_docstring=True)
def create_video(prompt: str) -> str:
    """Create a video based on the text description.

    Args:
        prompt: Description of the video content to be generated.
    """
    try:
        # 优化提示词
        optimized_prompt = _optimize_prompt(prompt)
        
        # 提交视频生成请求
        request_id = _submit_video_request(optimized_prompt)
        if not request_id:
            return "提交视频生成请求失败"
            
        print(f"视频生成请求已提交，requestId: {request_id}")
        
        # 获取视频URL并下载
        video_path = _get_video_url(request_id)
        if not video_path:
            return "视频生成失败"
            
        return video_path
        
    except Exception as e:
        return f"视频生成过程出错: {str(e)}"

tools = [create_video]
