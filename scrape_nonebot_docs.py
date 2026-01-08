"""
NoneBot API 文档爬虫
爬取 https://nonebot.dev/docs/api/ 的所有文档内容
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# 配置
BASE_URL = "https://nonebot.dev"
START_URL = "https://nonebot.dev/docs/api/"
OUTPUT_DIR = "nonebot_docs"
DELAY = 1  # 请求间隔（秒），避免对服务器造成压力

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def get_page(url: str) -> BeautifulSoup | None:
    """获取页面内容"""
    try:
        print(f"正在获取: {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"获取页面失败 {url}: {e}")
        return None


def extract_sidebar_links(soup: BeautifulSoup) -> list[dict]:
    """从侧边栏提取所有 API 文档链接"""
    links = []

    # 查找侧边栏菜单
    sidebar = soup.find("nav", class_="sidebar") or soup.find("aside") or soup.find("div", class_="sidebar")
    if not sidebar:
        # 尝试查找所有菜单链接
        sidebar = soup

    # 查找所有文档链接
    for link in sidebar.find_all("a", href=True):
        href = link.get("href", "")
        text = link.get_text(strip=True)

        # 只保留 /docs/api/ 下的链接
        if "/docs/api" in href and text:
            full_url = urljoin(BASE_URL, href)
            links.append({
                "title": text,
                "url": full_url
            })

    # 去重
    seen = set()
    unique_links = []
    for link in links:
        if link["url"] not in seen:
            seen.add(link["url"])
            unique_links.append(link)

    return unique_links


def extract_content(soup: BeautifulSoup) -> dict:
    """提取页面主要内容"""
    content = {
        "title": "",
        "description": "",
        "sections": []
    }

    # 提取标题
    title_elem = soup.find("h1")
    if title_elem:
        content["title"] = title_elem.get_text(strip=True)

    # 提取主要内容区域
    main_content = (
        soup.find("article") or
        soup.find("main") or
        soup.find("div", class_="theme-doc-markdown") or
        soup.find("div", class_="markdown")
    )

    if not main_content:
        main_content = soup

    # 提取所有段落和代码块
    sections = []
    current_section = {"heading": "", "content": []}

    for elem in main_content.find_all(["h1", "h2", "h3", "h4", "p", "pre", "ul", "ol", "li", "code"]):
        tag_name = elem.name

        if tag_name in ["h1", "h2", "h3", "h4"]:
            # 保存之前的 section
            if current_section["content"]:
                sections.append(current_section)
            current_section = {
                "heading": elem.get_text(strip=True),
                "level": int(tag_name[1]),
                "content": []
            }
        elif tag_name == "pre":
            # 代码块
            code = elem.get_text()
            current_section["content"].append({
                "type": "code",
                "text": code
            })
        elif tag_name == "p":
            text = elem.get_text(strip=True)
            if text:
                current_section["content"].append({
                    "type": "paragraph",
                    "text": text
                })
        elif tag_name in ["ul", "ol"]:
            items = [li.get_text(strip=True) for li in elem.find_all("li", recursive=False)]
            if items:
                current_section["content"].append({
                    "type": "list",
                    "items": items
                })

    # 保存最后一个 section
    if current_section["content"]:
        sections.append(current_section)

    content["sections"] = sections
    return content


def content_to_markdown(content: dict) -> str:
    """将提取的内容转换为 Markdown 格式"""
    lines = []

    if content["title"]:
        lines.append(f"# {content['title']}\n")

    if content["description"]:
        lines.append(f"{content['description']}\n")

    for section in content["sections"]:
        heading = section.get("heading", "")
        level = section.get("level", 2)

        if heading:
            lines.append(f"\n{'#' * level} {heading}\n")

        for item in section.get("content", []):
            item_type = item.get("type", "")

            if item_type == "paragraph":
                lines.append(f"{item['text']}\n")
            elif item_type == "code":
                lines.append(f"\n```python\n{item['text']}\n```\n")
            elif item_type == "list":
                for li in item.get("items", []):
                    lines.append(f"- {li}")
                lines.append("")

    return "\n".join(lines)


def save_content(filename: str, content: str):
    """保存内容到文件"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else OUTPUT_DIR, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"已保存: {filepath}")


def sanitize_filename(name: str) -> str:
    """清理文件名"""
    # 移除或替换不合法的文件名字符
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = name.strip('. ')
    return name or "unnamed"


def main():
    """主函数"""
    print("=" * 50)
    print("NoneBot API 文档爬虫")
    print("=" * 50)

    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 获取首页
    soup = get_page(START_URL)
    if not soup:
        print("无法获取首页，退出")
        return

    # 提取所有文档链接
    links = extract_sidebar_links(soup)
    print(f"\n找到 {len(links)} 个文档页面")

    # 如果没有找到链接，手动添加已知的 API 页面
    if len(links) < 5:
        print("侧边栏链接提取不完整，使用预定义链接列表...")
        links = [
            {"title": "nonebot", "url": "https://nonebot.dev/docs/api/"},
            {"title": "nonebot.config", "url": "https://nonebot.dev/docs/api/config"},
            {"title": "nonebot.message", "url": "https://nonebot.dev/docs/api/message"},
            {"title": "nonebot.matcher", "url": "https://nonebot.dev/docs/api/matcher"},
            {"title": "nonebot.params", "url": "https://nonebot.dev/docs/api/params"},
            {"title": "nonebot.rule", "url": "https://nonebot.dev/docs/api/rule"},
            {"title": "nonebot.permission", "url": "https://nonebot.dev/docs/api/permission"},
            {"title": "nonebot.log", "url": "https://nonebot.dev/docs/api/log"},
            {"title": "nonebot.utils", "url": "https://nonebot.dev/docs/api/utils"},
            {"title": "nonebot.consts", "url": "https://nonebot.dev/docs/api/consts"},
            {"title": "nonebot.exception", "url": "https://nonebot.dev/docs/api/exception"},
            {"title": "nonebot.typing", "url": "https://nonebot.dev/docs/api/typing"},
            {"title": "nonebot.plugin", "url": "https://nonebot.dev/docs/api/plugin/"},
            {"title": "nonebot.plugin.on", "url": "https://nonebot.dev/docs/api/plugin/on"},
            {"title": "nonebot.plugin.load", "url": "https://nonebot.dev/docs/api/plugin/load"},
            {"title": "nonebot.plugin.model", "url": "https://nonebot.dev/docs/api/plugin/model"},
            {"title": "nonebot.plugin.manager", "url": "https://nonebot.dev/docs/api/plugin/manager"},
            {"title": "nonebot.dependencies", "url": "https://nonebot.dev/docs/api/dependencies/"},
            {"title": "nonebot.drivers", "url": "https://nonebot.dev/docs/api/drivers/"},
            {"title": "nonebot.adapters", "url": "https://nonebot.dev/docs/api/adapters/"},
            {"title": "nonebot.compat", "url": "https://nonebot.dev/docs/api/compat"},
        ]

    # 打印找到的链接
    print("\n文档页面列表:")
    for i, link in enumerate(links, 1):
        print(f"  {i}. {link['title']} -> {link['url']}")

    # 爬取每个页面
    all_content = []
    for i, link in enumerate(links, 1):
        print(f"\n[{i}/{len(links)}] 正在处理: {link['title']}")

        page_soup = get_page(link["url"])
        if page_soup:
            content = extract_content(page_soup)
            content["url"] = link["url"]
            content["title"] = content["title"] or link["title"]

            # 保存为单独的 Markdown 文件
            filename = sanitize_filename(link["title"]) + ".md"
            markdown_content = content_to_markdown(content)
            save_content(filename, markdown_content)

            all_content.append(content)

        # 延迟，避免请求过快
        if i < len(links):
            time.sleep(DELAY)

    # 生成索引文件
    index_content = "# NoneBot API 文档索引\n\n"
    index_content += f"爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    index_content += "## 文档列表\n\n"

    for link in links:
        filename = sanitize_filename(link["title"]) + ".md"
        index_content += f"- [{link['title']}]({filename})\n"

    save_content("README.md", index_content)

    print("\n" + "=" * 50)
    print(f"爬取完成！共处理 {len(all_content)} 个页面")
    print(f"文档已保存到: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
