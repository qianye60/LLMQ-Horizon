"""
随机图片 API 工具
"""
import requests
from pathlib import Path
from datetime import datetime
from langchain_core.tools import tool
from .config import config

# 配置
picture_config = config.get("picture_api", {})
api_base = picture_config.get("api", "")

# 图片保存目录
root_path = Path(__file__).resolve().parents[1]
temp_dir = root_path / "temp_server" / "images"
temp_dir.mkdir(parents=True, exist_ok=True)

# 支持的图片类型
VALID_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "bmp"}


@tool(parse_docstring=True)
def random_picture(category: str) -> str:
    """获取随机图片

    Args:
        category: 图片分类，如 "beauty"(美女)、"anime"(动漫)、"scenery"(风景) 等
    """
    if not api_base:
        return "图片 API 未配置"

    try:
        # 请求图片
        response = requests.get(
            f"{api_base}{category}",
            timeout=15,
            allow_redirects=True
        )
        response.raise_for_status()

        # 获取文件扩展名
        url = response.url
        ext = url.split('.')[-1].lower().split('?')[0]

        if ext not in VALID_EXTENSIONS:
            ext = "jpg"

        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"random_{category}_{timestamp}.{ext}"
        save_path = temp_dir / filename

        # 保存图片
        save_path.write_bytes(response.content)
        print(f"图片已保存: {save_path}")

        return url

    except requests.exceptions.Timeout:
        return "图片获取超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        print(f"图片 API 请求失败: {e}")
        return "图片获取失败"
    except Exception as e:
        print(f"图片处理出错: {e}")
        return "图片处理出错"


tools = [random_picture]
