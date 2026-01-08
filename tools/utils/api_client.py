"""
公共 API 调用工具
提供统一的 HTTP 请求、提示词优化、重试机制等功能
"""
import requests
import time
from typing import Optional, Dict, Any, Callable
from functools import wraps


class APIClient:
    """统一的 API 客户端"""

    def __init__(
        self,
        base_url: str,
        api_key: str = None,
        timeout: int = 30,
        max_retries: int = 2,
        backoff_factor: float = 2.0
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _get_headers(self, extra_headers: Dict[str, str] = None) -> Dict[str, str]:
        """构建请求头"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Optional[requests.Response]:
        """带重试机制的请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if endpoint else self.base_url
        kwargs.setdefault('timeout', self.timeout)

        retry_count = 0
        last_error = None

        while retry_count < self.max_retries:
            try:
                response = requests.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.Timeout:
                last_error = "请求超时"
            except requests.exceptions.HTTPError as e:
                if e.response.status_code >= 500:
                    last_error = f"服务器错误: {e.response.status_code}"
                else:
                    raise
            except requests.exceptions.RequestException as e:
                last_error = str(e)

            retry_count += 1
            if retry_count < self.max_retries:
                time.sleep(self.backoff_factor ** retry_count)

        raise requests.exceptions.RequestException(f"请求失败 (重试 {self.max_retries} 次后): {last_error}")

    def get(self, endpoint: str = "", params: Dict = None, headers: Dict = None) -> requests.Response:
        """GET 请求"""
        return self._request_with_retry(
            "GET",
            endpoint,
            params=params,
            headers=self._get_headers(headers)
        )

    def post(self, endpoint: str = "", json: Dict = None, data: Any = None, headers: Dict = None) -> requests.Response:
        """POST 请求"""
        return self._request_with_retry(
            "POST",
            endpoint,
            json=json,
            data=data,
            headers=self._get_headers(headers)
        )


def optimize_prompt(
    prompt: str,
    prompt_type: str,
    api_key: str,
    base_url: str,
    model: str,
    prompt_templates: Dict[str, str],
    timeout: int = 30
) -> str:
    """统一的提示词优化函数

    Args:
        prompt: 原始提示词
        prompt_type: 提示词类型（如 "create_art", "create_video"）
        api_key: OpenAI 格式 API 密钥
        base_url: API 基础 URL
        model: 模型名称
        prompt_templates: 提示词模板字典
        timeout: 超时时间

    Returns:
        优化后的提示词，失败时返回原始提示词
    """
    system_prompt = prompt_templates.get(prompt_type)
    if not system_prompt:
        print(f"未找到 {prompt_type} 的提示词模板，使用原始提示词")
        return prompt

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()

        result = response.json()
        if result.get("choices") and len(result["choices"]) > 0:
            optimized = result["choices"][0]["message"]["content"].strip()
            print(f"优化后的提示词: [{optimized}]")
            return optimized

        print("提示词优化失败，使用原始提示词")
        return prompt

    except requests.exceptions.RequestException as e:
        print(f"提示词优化请求失败: {e}")
        return prompt
    except Exception as e:
        print(f"提示词优化出错: {e}")
        return prompt


def with_retry(max_retries: int = 2, backoff_factor: float = 2.0):
    """重试装饰器"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        time.sleep(backoff_factor ** (attempt + 1))
            raise last_error
        return wrapper
    return decorator


# 常用的尺寸映射
SIZE_MAPPINGS = {
    "square": {"width": 1024, "height": 1024, "ratio": "1:1"},
    "portrait": {"width": 576, "height": 1024, "ratio": "9:16"},
    "landscape": {"width": 1024, "height": 576, "ratio": "16:9"},
}


def get_size_params(size: str, format_type: str = "dict") -> Any:
    """获取尺寸参数

    Args:
        size: 尺寸类型 (square/portrait/landscape)
        format_type: 返回格式 (dict/string/tuple)

    Returns:
        对应格式的尺寸参数
    """
    size_info = SIZE_MAPPINGS.get(size, SIZE_MAPPINGS["square"])

    if format_type == "string":
        return f"{size_info['width']}x{size_info['height']}"
    elif format_type == "tuple":
        return (size_info['width'], size_info['height'])
    else:
        return {"width": size_info['width'], "height": size_info['height']}
