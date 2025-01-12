import requests
from .config import config
from langchain_core.tools import tool

get_news_config = config.get("get_news", {})
base_url = get_news_config.get("base_url", "")
    
@tool(parse_docstring=True)
def get_news(category: str = None, limit: int = 10) -> str:
    """Get news.
    
    Args:
        category: The category of news, Defaults None, valid values: "Economy", "Education", "Entertainment", "Environment", "Military", "Other", "Politics", "Society", "Sports", "Technology".
        limit: The number of news to get
    """
    try:
        params = {'limit': limit}
        if category is not None:
            params['category'] = category
            
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
    except Exception as e:
        return {"error": f"Unknown error: {str(e)}"}

tools = [get_news]

