"""
Jina AI 统一 API 工具
合并了搜索、网页读取、事实核查三个功能
"""
import requests
from langchain_core.tools import tool
from .config import config

jina_config = config.get('jina', {})
jina_api_key = jina_config.get('api_key', '')
top_n = jina_config.get('top_n', 30)
min_length = jina_config.get('min_length', 10)

# API 端点映射
JINA_ENDPOINTS = {
    "search": "s.jina.ai",      # 搜索
    "reader": "r.jina.ai",      # 网页内容提取
    "grounding": "g.jina.ai",   # 事实核查/Grounding
}


def _call_jina_api(query: str, api_type: str, timeout: int = 30) -> str:
    """统一的 Jina API 调用

    Args:
        query: 查询内容或 URL
        api_type: API 类型 (search/reader/grounding)
        timeout: 超时时间（秒）

    Returns:
        处理后的结果文本
    """
    endpoint = JINA_ENDPOINTS.get(api_type)
    if not endpoint:
        return f"不支持的 API 类型: {api_type}"

    url = f'https://{endpoint}/{query}'

    headers = {
        'X-Retain-Images': 'none'
    }

    if api_type == "grounding":
        headers['Accept'] = 'application/json'

    if jina_api_key:
        headers['Authorization'] = f'Bearer {jina_api_key}'

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        lines = response.text.splitlines()
        filtered_lines = [line for line in lines if len(line.strip()) >= min_length]
        truncated_lines = filtered_lines[:top_n]
        result = '\n'.join(truncated_lines)

        return result if result else "未找到相关内容"
    except requests.exceptions.Timeout:
        return "请求超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        return f"请求失败: {str(e)}"


@tool(parse_docstring=True)
def web_search(query: str) -> str:
    """在搜索引擎中搜索信息

    Args:
        query: 要搜索的内容/关键词
    """
    return _call_jina_api(query, "search", timeout=30)


@tool(parse_docstring=True)
def read_url(url: str) -> str:
    """获取网页URL的内容

    Args:
        url: 要获取内容的网页URL
    """
    return _call_jina_api(url, "reader", timeout=20)


@tool(parse_docstring=True)
def fact_check(query: str) -> str:
    """事实核查 - 验证某个事实或获取准确信息

    Args:
        query: 需要核查的事实内容，如"OpenAI o1-pro的订阅价格是多少"
    """
    return _call_jina_api(query, "grounding", timeout=30)


tools = [web_search, read_url, fact_check]
