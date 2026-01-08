"""
仙途游戏帮助工具 - 提供游戏介绍、配置教程、常见问题解答
"""
from pathlib import Path
from langchain_core.tools import tool

# 游戏文档目录
XIANTU_DIR = Path(__file__).resolve().parents[1] / "仙途"


# ==================== 游戏介绍 ====================
GAME_INTRO = '''
🎮 仙途（Xian Tu）- AI 驱动的沉浸式修仙文字冒险游戏

✨ 游戏特色：
• 🤖 AI 动态叙事 - 支持 Gemini/Claude/OpenAI/DeepSeek 等多种大模型
• ⚔️ 完整修仙体系 - 境界突破、三千大道、功法修炼、装备炼制
• 🎲 智能判定系统 - 多维度计算判定结果
• 💾 多存档管理 - 多角色、多存档槽位
• 🗺️ 开放世界 - 自由探索朝天大陆
• 🍺 酒馆兼容 - 支持 SillyTavern 嵌入式环境

🌐 在线体验：https://www.ddct.top/
💬 QQ群：1079437686
📖 详细介绍：https://qianye60.github.io/XianTu/游戏介绍.html
'''


# ==================== SillyTavern 配置教程 ====================
SILLYTAVERN_GUIDE = '''
🍺 SillyTavern（酒馆）配置教程

📥 第一步：下载安装酒馆
1. 前往 https://github.com/SillyTavern/SillyTavern 下载
2. Windows 用户运行 Start.bat
3. 浏览器访问 http://localhost:8000

⚙️ 第二步：配置 API
1. 点击右上角 ⚙️ 设置图标
2. 选择 "API Connections"
3. 选择你要使用的 API 类型：

   【OpenAI / 兼容 API】
   - API Type: OpenAI
   - API Key: 你的 API 密钥
   - API URL: API 地址（注意删除末尾的 /v1）

   【Claude】
   - API Type: Claude
   - API Key: 你的 Anthropic API 密钥

   【Google Gemini】
   - API Type: Google AI
   - API Key: 你的 Google API 密钥

🎴 第三步：导入仙途角色卡
1. 下载仙途角色卡 PNG 图片
2. 在酒馆中点击 "Characters" → "Import"
3. 选择下载的角色卡图片导入

▶️ 第四步：开始游戏
1. 在角色列表中点击仙途角色卡
2. 点击 "Start Chat" 开始游戏
3. 按照游戏提示创建角色

💡 常见问题：
• API 连接失败 → 检查 API Key 是否正确，URL 是否正确
• 响应很慢 → 检查网络，或切换其他 API 提供商
• 格式错误 → 更新到最新版本角色卡
'''


# ==================== API 配置教程 ====================
API_CONFIG_GUIDE = '''
🔑 API 配置教程

【方式一：使用官方 API】

1️⃣ OpenAI API
   - 官网：https://platform.openai.com
   - 获取 Key：API Keys → Create new secret key
   - 推荐模型：gpt-4o, gpt-4-turbo

2️⃣ Google Gemini API（推荐，免费额度高）
   - 官网：https://aistudio.google.com
   - 获取 Key：Get API Key → Create API key
   - 推荐模型：gemini-1.5-pro, gemini-2.0-flash

3️⃣ Anthropic Claude API
   - 官网：https://console.anthropic.com
   - 获取 Key：API Keys → Create Key
   - 推荐模型：claude-3-5-sonnet

4️⃣ DeepSeek API（性价比高）
   - 官网：https://platform.deepseek.com
   - 获取 Key：API Keys → 创建 API Key
   - 推荐模型：deepseek-chat

【方式二：使用中转 API】

中转 API 可以用国内网络访问，价格通常更便宜：
• 在 Google 搜索 "OpenAI 中转 API"
• 注册获取 API Key 和 Base URL
• 配置时填写中转商提供的地址

【配置注意事项】

⚠️ API URL 格式：
   ✅ 正确：https://api.openai.com
   ❌ 错误：https://api.openai.com/v1（不要加 /v1）

⚠️ 模型选择：
   • 长对话推荐高上下文模型
   • gemini-1.5-pro 支持 100 万 tokens
   • gpt-4-turbo 支持 128k tokens

⚠️ Token 用量：
   • 仙途单次对话约消耗 2000-5000 tokens
   • 建议选择有足够余额的 API
'''


# ==================== 常见问题 ====================
FAQ = '''
❓ 仙途常见问题解答

【安装问题】

Q: 酒馆打不开怎么办？
A: 确保已安装 Node.js，运行 Start.bat 时注意看报错信息

Q: 角色卡导入失败？
A: 确保下载的是完整的 PNG 图片，不要用截图

Q: 网页版打不开？
A: 访问 https://www.ddct.top/，确保网络正常

【API 问题】

Q: API 连接失败？
A:
   1. 检查 API Key 是否正确（无多余空格）
   2. 检查 API URL 格式（不要加 /v1）
   3. 检查网络是否能访问 API 地址
   4. 使用"API 测试"功能验证连接

Q: 响应很慢怎么办？
A:
   1. 检查网络延迟
   2. 尝试切换其他 API 提供商
   3. 使用响应更快的模型

Q: Token 用完了？
A: 充值或更换其他 API 提供商

【游戏问题】

Q: AI 输出格式错误？
A: 更新到最新版本角色卡，使用推荐的模型

Q: 存档丢失了？
A:
   1. 检查浏览器是否清除了缓存
   2. 建议定期导出存档备份

Q: 如何多开存档？
A: 游戏内支持多存档槽位，可创建多个角色

Q: 如何联机共修？
A: 需要部署后端服务，详见项目文档

【其他问题】

Q: 如何获取最新版本？
A:
   1. 酒馆版：重新下载角色卡（自动更新）
   2. 网页版：直接访问官网（自动更新）

Q: 如何反馈问题？
A: 加入 QQ 群 1079437686 反馈
'''


# ==================== 更新日志摘要 ====================
def get_changelog_summary() -> str:
    """获取更新日志摘要"""
    changelog_file = XIANTU_DIR / "CHANGELOG.md"
    if not changelog_file.exists():
        return "暂无更新日志"

    try:
        content = changelog_file.read_text(encoding="utf-8")
        # 只取前 2000 字符作为摘要
        lines = content.split('\n')
        summary_lines = []
        count = 0
        for line in lines:
            summary_lines.append(line)
            count += len(line)
            if count > 2000:
                summary_lines.append("\n... (更多内容请查看完整更新日志)")
                break
        return '\n'.join(summary_lines)
    except Exception as e:
        return f"读取更新日志失败: {e}"


@tool(parse_docstring=True)
def xiantu_help(topic: str = "intro") -> str:
    """仙途游戏帮助工具 - 提供游戏介绍、配置教程、常见问题解答

    Args:
        topic: 帮助主题，可选值为 intro(游戏介绍)、tavern(SillyTavern配置教程)、api(API配置教程)、faq(常见问题解答)、changelog(最新更新日志)、all(显示所有帮助信息)
    """
    topic_map = {
        "intro": GAME_INTRO,
        "tavern": SILLYTAVERN_GUIDE,
        "api": API_CONFIG_GUIDE,
        "faq": FAQ,
        "changelog": get_changelog_summary,
    }

    if topic == "all":
        return f"{GAME_INTRO}\n\n{SILLYTAVERN_GUIDE}\n\n{API_CONFIG_GUIDE}\n\n{FAQ}"

    if topic in topic_map:
        result = topic_map[topic]
        if callable(result):
            return result()
        return result

    return f"未知主题: {topic}。可选: intro/tavern/api/faq/changelog/all"


tools = [xiantu_help]
