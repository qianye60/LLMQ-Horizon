# tools/picture_api.py
import requests
from langchain_core.tools import tool
from .config import config
import os

picture = config.get("picture_api", {})
api = picture.get("api")

@tool(parse_docstring=True)
def picture_api(select_type: str="动漫") -> str:
    """根据请求从变量api_type_list选择合适的图片分类请求随机图片api，将图片存储到服务器并且返回图片链接。
    
    Args:
      select_type: 优先根据用户请求匹配图片类型，图片类型有["动漫","美好"]，用户没有指定或是指定列表中不存在的将默认使用"动漫"类型。
    """
    try:
      # 获取当前脚本的绝对路径
      current_dir = os.path.dirname(os.path.abspath(__file__))
      # 获取上级目录的路径
      parent_dir = os.path.dirname(current_dir)
      #请求url
      pic_response = requests.get(api+select_type)
      if pic_response:
        pic_type = pic_response.url.split('.')[-1]
        print(pic_response.url)
        with open(parent_dir+"/temp_server/random."+pic_type, 'wb') as f:
          f.write(pic_response.content)
        return pic_response.url
    except Exception as e:
      print(f"picture_api出现错误: {e}")
      return None
tools = [picture_api]
