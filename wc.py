import requests
from typing import Optional, List
from datetime import date

def get_news(
    base_url: str,
    keywords: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    start_time: Optional[date] = None,
    end_time: Optional[date] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = None
) -> dict:
    """
    获取新闻数据
    
    Args:
        base_url: API基础URL，例如 "http://api.example.com"
        keywords: 搜索关键词，多个关键词用逗号分隔
        category: 新闻分类
        country: 新闻国家（使用ISO 3166-1 alpha-2代码，如CN、US等）
        start_time: 开始时间
        end_time: 结束时间
        order_by: 排序方式（time_asc:时间升序, time_desc:时间降序, random:随机排序）
        limit: 返回新闻数量 (默认: 10, 最大: 50)
    
    Returns:
        dict: 包含新闻数据的字典
    """
    endpoint = f"{base_url.rstrip('/')}/news"
    
    # 构建查询参数
    params = {}
    if keywords:
        params['keywords'] = keywords
    if category:
        params['category'] = category
    if country:
        params['country'] = country
    if start_time:
        params['start_time'] = start_time.strftime('%Y-%m-%d')
    if end_time:
        params['end_time'] = end_time.strftime('%Y-%m-%d')
    if order_by:
        params['order_by'] = order_by
    if limit:
        params['limit'] = limit
        
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # 如果响应状态码不是200，抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"获取新闻失败: {str(e)}")

# 使用示例
if __name__ == "__main__":
    # 示例用法
    try:
        news_data = get_news(
            base_url="http://127.0.0.1:8080",
            keywords="科技,AI",
            category="technology",
            country="CN",
            limit=10
        )
        print(news_data)
    except Exception as e:
        print(f"错误: {e}")
