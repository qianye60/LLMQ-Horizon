from langchain_core.tools import tool
from typing import Dict, Union
from datetime import datetime
from .config import config
import requests
import pytz
import os

weather_config = config.get('get_weather_data', {})
OPENWEATHER_API_KEY = weather_config.get('api_key', '')
print(OPENWEATHER_API_KEY)
def get_coordinates(location: str, country_code: str, api_key: str) -> Union[tuple[float, float], str]:
    """根据城市名和国家代码获取地理坐标，返回坐标元组或错误消息。"""
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={location},{country_code}&limit=1&appid={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            lat, lon = data[0]['lat'], data[0]['lon']
            print(f"成功获取 {location}, {country_code} 的坐标: 纬度={lat}, 经度={lon}")
            return lat, lon
        else:
            error_msg = f"未找到城市 '{location}', 国家代码 '{country_code}' 的坐标信息。"
            print(error_msg)
            return error_msg
    except requests.exceptions.RequestException as e:
        error_msg = f"获取坐标时发生网络错误: {type(e).__name__}: {e}"
        print(error_msg)
        return error_msg
    except ValueError as e:
        error_msg = f"解析坐标响应时发生错误: {e}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"获取坐标时发生未知错误: {e}"
        print(error_msg)
        return error_msg

def _format_timestamp(timestamp: int | float, timezone_str: str) -> str | int | float:
    """格式化时间戳为指定时区的日期时间字符串。"""
    try:
        tz = pytz.timezone(timezone_str)
        dt = datetime.fromtimestamp(timestamp, tz)
        return dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"警告: 未知的时区 '{timezone_str}'，无法格式化时间戳。")
        return timestamp
    except Exception as e:
        print(f"警告: 格式化时间戳时发生错误: {e}")
        return timestamp

def _format_timestamps_in_data(data: dict | list, timezone_str: str) -> dict | list:
    """递归地格式化 JSON 数据中的时间戳字段。"""
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ('dt', 'sunrise', 'sunset', 'moonrise', 'moonset') and isinstance(value, (int, float)):
                data[key] = _format_timestamp(value, timezone_str)
            elif isinstance(value, (dict, list)):
                _format_timestamps_in_data(value, timezone_str)
    elif isinstance(data, list):
        for item in data:
            _format_timestamps_in_data(item, timezone_str)
    return data

def get_onecall_weather(latitude: float, longitude: float, api_key: str, exclude: list[str] | None = None) -> Union[Dict, str]:
    """使用 OpenWeatherMap One Call API 获取天气数据并格式化时间戳，返回数据字典或错误消息。"""
    base_url = 'https://api.openweathermap.org/data/3.0/onecall'
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': api_key,
        'units': 'metric',
        'exclude': ','.join(exclude) if exclude else None
    }
    try:
        print(f"请求天气数据中... (纬度={latitude}, 经度={longitude})")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'timezone' in data:
            data = _format_timestamps_in_data(data, data['timezone'])
        print(f"成功获取天气数据。状态码: {response.status_code}")
        return data
    except requests.exceptions.RequestException as e:
        error_msg = f"获取天气数据时发生网络错误: {type(e).__name__}: {e}"
        print(error_msg)
        return error_msg
    except ValueError as e:
        error_msg = f"解析天气数据响应时发生错误: {e}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"获取天气数据时发生未知错误: {e}"
        print(error_msg)
        return error_msg


@tool(parse_docstring=True)
def get_weather_data(location: str, country_code: str, forecast_type: str = "future_48h_weather") -> Union[Dict, str]:
    """Use OpenWeather to get current weather data, 48-hour forecast, and 8-day forecast.

    Args:
        location (str): City name.  e.g. 长沙, London.
        country_code (str): The ISO 3166 country code for the location.  e.g. CN, US, GB.
        forecast_type (str): The requested weather forecast type.  Available options: "future_48h_weather" (next 48 hours' weather), "future_8day_weather" (next 8 days' weather).
    """
    print(f"开始获取 {location}, {country_code} 的 {forecast_type} 天气预报...")
    api_key = OPENWEATHER_API_KEY
    geo_result = get_coordinates(location, country_code, api_key)
    if isinstance(geo_result, str):
        return f"获取坐标失败: {geo_result}"
    lat, lon = geo_result

    exclude_map = {
        'future_48h_weather': ['current', 'daily'],
        'future_8day_weather': ['current', 'hourly'],
    }
    if forecast_type not in exclude_map:
        error_msg = f"错误的预报类型: '{forecast_type}'。请选择 'future_48h_weather' 或 'future_8day_weather'。"
        print(error_msg)
        return error_msg

    exclude_list = ['alerts', 'minutely'] + exclude_map[forecast_type]

    weather_result = get_onecall_weather(lat, lon, api_key, exclude=exclude_list)
    if isinstance(weather_result, str):
        return f"获取天气数据失败: {weather_result}"

    return weather_result

tools = [get_weather_data]