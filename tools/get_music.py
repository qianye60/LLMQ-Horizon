import requests
import yt_dlp
import os
import re
from langchain_core.tools import tool
from pathlib import Path
from difflib import SequenceMatcher

root_path = Path(__file__).resolve().parents[1]
CACHE_DIR = root_path / "temp_server" / "audio"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def ensure_dir_exists(directory):
    """
    确保指定的目录存在，否则创建。
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def search_netease_music(
    music_name, search_type=1, limit=3
):
    """
    在网易云音乐上搜索歌曲，并返回结果列表。

    Args:
        music_name (str): 搜索关键词
        search_type (int): 搜索类型，1 表示单曲
        limit (int): 返回结果数量
    """
    search_url = f"https://music.163.com/api/search/get?s={music_name}&type={search_type}&limit={limit}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()

        if data and data['code'] == 200 and data['result'] and data['result']['songs']:
            songs = data['result']['songs']
            results = []
            for song in songs:
                song_id = song['id']
                song_name = song['name']
                song_url = f"https://music.163.com/#/song?id={song_id}"
                results.append({
                    'id': song_id,
                    'name': song_name,
                    'url': song_url
                })
            return results
        else:
            print("未找到相关歌曲或解析结果失败")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None

def normalize_filename(filename: str) -> str:
    """
    规范化文件名：
    - 移除特殊字符
    - 将空格替换为下划线
    - 仅保留字母、数字、下划线和中文字符
    """
    # 保留字母、数字、下划线和中文字符，其他替换为空格
    normalized = re.sub(r'[^\w\u4e00-\u9fff]', ' ', filename)
    # 将连续空格替换为单个下划线
    normalized = re.sub(r'\s+', '_', normalized.strip())
    return normalized

def get_cached_filename(song_url, output_dir="."):
    """
    根据歌曲URL和缓存目录生成规范化的缓存文件名。

    Args:
        song_url: 歌曲的URL
        output_dir: 下载目录

    Returns:
        缓存文件的完整路径，如果无法获取文件名，返回 None
    """
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(song_url, download=False)
            original_filename = ydl.prepare_filename(info_dict)
            
            # 规范化文件名部分
            base_name = os.path.splitext(os.path.basename(original_filename))[0]
            ext = os.path.splitext(original_filename)[1]
            normalized_name = normalize_filename(base_name)
            
            return os.path.join(os.path.dirname(original_filename), f"{normalized_name}{ext}")
        except yt_dlp.DownloadError as e:
            print(f"获取文件名出错: {e}")
            return None

def find_similar_cache(music_name, min_match_ratio=0.4):
    """
    根据音乐名称查找相似的缓存文件路径。

    Args:
        music_name (str): 音乐名称
        min_match_ratio (float): 最小匹配率 (0-1)
    """
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR, exist_ok=True)

    cached_files = os.listdir(CACHE_DIR)
    similar_files = []

    # 对搜索关键词进行分词
    music_name = music_name.lower()
    keywords = music_name.split()
    if not keywords:
        keywords = [music_name]

    for filename in cached_files:
        name, ext = os.path.splitext(filename)
        name = name.lower()
        
        # 对文件名进行分词
        name_parts = name.split()
        if not name_parts:
            name_parts = [name]

        # 检查关键词匹配
        matches = 0
        for keyword in keywords:
            for part in name_parts:
                ratio = SequenceMatcher(None, part, keyword).ratio()
                if ratio >= 0.8:
                    matches += 1
                    break

        # 计算匹配率
        match_ratio = matches / max(len(keywords), 1)
            
        if match_ratio >= min_match_ratio:
            file_path = os.path.join(CACHE_DIR, filename)
            similar_files.append((file_path, os.path.getsize(file_path), match_ratio))

    if similar_files:
        # 首先按匹配率排序，然后按文件大小排序
        sorted_files = sorted(similar_files, key=lambda x: (-x[2], -x[1]))
        return sorted_files[0][0]
    else:
        return None

def download_song_by_url(song_url, output_dir="."):
    """
    使用 yt_dlp 根据歌曲 URL 下载歌曲。

    Args:
        song_url (str): 歌曲的 URL
        output_dir (str): 下载目录，默认为当前目录
    """
    cache_filename = get_cached_filename(song_url, CACHE_DIR)

    if cache_filename and os.path.exists(cache_filename):
        print(f"已存在缓存文件: {cache_filename}")
        return cache_filename  # 返回缓存文件路径

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
    }

    ensure_dir_exists(CACHE_DIR)
    ensure_dir_exists(output_dir)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(song_url, download=False)
            song_name = info_dict.get("title", "Unknown Song")
            print(f"正在下载: {song_name} ({song_url})")

            ydl.download([song_url])
            return get_cached_filename(song_url, output_dir) # 返回下载后的文件路径
        except yt_dlp.DownloadError as e:
            print(f"下载 {song_url} 出错: {e}")
            return None

def download_first_netease_music(keyword, search_type=1, limit=3, output_dir="."):
    """
    搜索歌曲并下载第一个结果

    Args:
        keyword: 搜索关键词
        search_type: 搜索类型，1 表示单曲
        limit: 搜索结果数量限制
        output_dir: 下载目录，默认为当前目录
    """
    ensure_dir_exists(CACHE_DIR)
    search_results = search_netease_music(keyword, search_type, limit)

    if search_results:
        first_song_url = search_results[0]['url']
        return download_song_by_url(first_song_url, CACHE_DIR)
    else:
        print("没有找到可以下载的歌曲")
        return None


def _get_hhlq_music(music_name) -> str:
    """
    调用红海龙淇 API 获取音乐，并下载到缓存目录。

    Args:
        music_name (str): 音乐名称
    """
    try:
        response = requests.get(
            f"https://www.hhlqilongzhu.cn/api/dg_wyymusic.php?gm={music_name}&n=1&num=1&type=json"
        )
        music_url = re.search(r"^(https?://[^\s]+?\.mp3)", response.json()["music_url"]).group(0)
        
        # 下载到缓存目录, 并重新命名
        filename = download_to_cache(music_url, music_name)
        return filename if filename else "下载失败"

    except Exception as e:
        return f"Failed to get music link: {str(e)}"
    
def download_to_cache(url, music_name):
    """
    通过普通请求下载文件到缓存目录并以规范化的歌曲名命名。

    Args:
        url (str): 文件 URL
        music_name (str): 音乐名称
    """
    ensure_dir_exists(CACHE_DIR)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 规范化音乐名称
        normalized_name = normalize_filename(music_name)
        
        # 获取原始文件扩展名
        original_filename = url.split("/")[-1]
        ext = os.path.splitext(original_filename)[1]
        
        # 组合最终的文件名
        filename = os.path.join(CACHE_DIR, f"{normalized_name}{ext}")
        
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename
    except Exception as e:
        print(f"下载 {url} 到缓存出错: {e}")
        return None


@tool(parse_docstring=True)
def get_music(music_name: str, provider: str = "hhlq") -> str:
    """Search and acquire music.

    Args:
        music_name (str): music name e.g. "邓紫棋泡沫"
        provider (str): Music provider. Available values: "hhlq", "netease"
    """
    # 1. 检查缓存
    cached_file = find_similar_cache(music_name)
    if cached_file:
        print(f"使用缓存: {cached_file}")
        return f"file://{cached_file}"

    # 2. 根据提供商路由
    provider_map = {
        "hhlq": _get_hhlq_music,
        "netease": download_first_netease_music,
    }

    if provider in provider_map:
        result = provider_map[provider](music_name)
        if provider == "hhlq" and (result == "下载失败" or "Failed to get music link" in result):
            print("hhlq API 下载失败，尝试使用网易云音乐")
            result = provider_map["netease"](music_name)
        return f"file://{result}"
    
    else:
        return "Unsupported music API provider"

tools = [get_music]

# if __name__ == "__main__":
#     print(get_music(music_name="邓紫棋泡沫"))
    # print(get_music(music_name="泡沫", provider="hhlq"))
