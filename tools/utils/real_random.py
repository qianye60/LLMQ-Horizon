import requests
import json

def get_random_numbers(api_key, num_integers, min_val, max_val, replacement=True, base=10, pregeneratedRandomization=None):
    """
    从 random.org 的 Basic API 获取真正的随机整数。
    """
    url = "https://api.random.org/json-rpc/4/invoke"
    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": api_key,
            "n": num_integers,
            "min": min_val,
            "max": max_val,
            "replacement": replacement,
            "base": base
        },
        "id": 42
    }
    if pregeneratedRandomization is not None:
        payload["params"]["pregeneratedRandomization"] = pregeneratedRandomization

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        result = response.json()
        if "result" in result and "random" in result["result"] and "data" in result["result"]["random"]:
            return result["result"]["random"]["data"]
        else:
            print(f"Error: Unexpected response format: {result}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return None

if __name__ == "main":
    get_random_numbers()