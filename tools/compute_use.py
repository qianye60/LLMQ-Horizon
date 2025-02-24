import requests
from langchain_core.tools import tool
from .config import config

compute_use_config = config.get("compute_use", {})
base_url = compute_use_config.get("base_url", "http://localhost:3000")  # Default if not in config

@tool(parse_docstring=True)
def compute_use(task: str) -> str:
    """Execute the given tasks or operations in the computer browser.

    Args:        
      task: Detailed description of the detailed steps of tasks or operations to be performed in the browser (note that there is no need to open the browser), for example: 1. First, open Bing; 2. Next, xxx; 3. Finally, xxx
    """
    try:
        url = base_url
        headers = {"Content-Type": "application/json"}
        data = {"task": task}
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()

        result = response.json()
        if "error" in result:
            return {"error": result["error"]}
        elif "result" in result:
            return result["result"] 
        else:
            return {"error": "The server returned an unexpected response format."}


    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please check if the server is running or if the task is too complex."}
    except requests.exceptions.ConnectionError as e:
        return {"error": f"Connection error: {e}. Please check your network connection or the server address."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

tools = [compute_use]
