import requests
from typing import Optional
from .config import config
from langchain_core.tools import tool

get_news_config = config.get("get_news", {})
base_url = get_news_config.get("base_url", "")
    
@tool(parse_docstring=True)
def get_news(
    category: Optional[str] = None,
    keywords: Optional[str] = None,
    country: Optional[str] = None,
    order_by: Optional[str] = None,
    limit: int = 10
) -> str:
    """Get news data. Returns 10 random news items from today if no parameters are provided.
    
    Args:
        category: News category, valid values: "technology", "medicine", "finance", "politics", "society", "sports", "culture", "education", "science", "military", "environment", "life", "entertainment", "other"
        keywords: Search keywords, multiple keywords separated by commas
        country: News country (using ISO 3166-1 alpha-2 code, e.g., CN, US)
        order_by: Sort order (time_asc: ascending by time, time_desc: descending by time, random: random order)
        limit: Number of news items to return (default: 10, max: 50)
    """
    try:
        # 参数验证
        if limit > 50:
            return {"error": "Limit cannot exceed 50"}
            
        if category and category not in [
            "technology", "medicine", "finance", "politics", "society", 
            "sports", "culture", "education", "science", "military", 
            "environment", "life", "entertainment", "other"
        ]:
            return {"error": "Invalid category"}
            
        if order_by and order_by not in ["time_asc", "time_desc", "random"]:
            return {"error": "Invalid order_by value"}

        # 构建查询参数
        params = {'limit': limit}
        if category:
            params['category'] = category
        if keywords:
            params['keywords'] = keywords
        if country:
            params['country'] = country
        if order_by:
            params['order_by'] = order_by
            
        url = f"{base_url}/news"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get('code') != 200:
            return {"error": result.get('message', 'Unknown error')}
            
        news_list = result.get('data', [])
        if not news_list:
            return {"error": "No news found"}

        return news_list
        
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"Invalid parameter value: {str(e)}"}
    except Exception as e:
        return {"error": f"Unknown error: {str(e)}"}

tools = [get_news]

