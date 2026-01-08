"""
帮助菜单工具 - 生成功能菜单图片
"""
from pathlib import Path
from datetime import datetime
from langchain_core.tools import tool
from nonebot import logger

# 图片保存目录
ROOT_PATH = Path(__file__).resolve().parents[1]
MENU_DIR = ROOT_PATH / "temp_server" / "menu"
MENU_DIR.mkdir(parents=True, exist_ok=True)

# 尝试导入imgkit
try:
    import imgkit
    IMGKIT_AVAILABLE = True
except ImportError:
    IMGKIT_AVAILABLE = False
    logger.warning("imgkit未安装，菜单图片功能不可用。请运行: pip install imgkit")


def generate_menu_html() -> str:
    """生成菜单 HTML"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .header h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 14px;
        }
        .section {
            margin-bottom: 25px;
        }
        .section-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            padding: 10px 15px;
            background: linear-gradient(90deg, #f0f4ff 0%, transparent 100%);
            border-left: 4px solid #667eea;
            border-radius: 0 10px 10px 0;
        }
        .commands {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .command {
            background: #f8f9fa;
            padding: 12px 15px;
            border-radius: 10px;
            border: 1px solid #eee;
        }
        .command-name {
            font-weight: bold;
            color: #667eea;
            font-size: 14px;
        }
        .command-desc {
            color: #666;
            font-size: 12px;
            margin-top: 5px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #999;
            font-size: 12px;
        }
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 10px;
            margin-left: 5px;
        }
        .tag-admin { background: #fff3cd; color: #856404; }
        .tag-super { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 机器人功能菜单</h1>
            <p>使用 @机器人 或触发词唤醒，然后说出你的需求</p>
        </div>

        <div class="section">
            <div class="section-title">💬 基础功能</div>
            <div class="commands">
                <div class="command">
                    <div class="command-name">智能对话</div>
                    <div class="command-desc">直接 @机器人 或使用触发词进行对话</div>
                </div>
                <div class="command">
                    <div class="command-name">网络搜索</div>
                    <div class="command-desc">搜索最新信息、查询知识</div>
                </div>
                <div class="command">
                    <div class="command-name">天气查询</div>
                    <div class="command-desc">查询任意城市的天气信息</div>
                </div>
                <div class="command">
                    <div class="command-name">网页阅读</div>
                    <div class="command-desc">获取网页链接的内容摘要</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🎨 创作功能</div>
            <div class="commands">
                <div class="command">
                    <div class="command-name">AI 绘画</div>
                    <div class="command-desc">根据描述生成图片</div>
                </div>
                <div class="command">
                    <div class="command-name">语音合成</div>
                    <div class="command-desc">将文字转换为语音</div>
                </div>
                <div class="command">
                    <div class="command-name">视频生成</div>
                    <div class="command-desc">根据描述生成短视频</div>
                </div>
                <div class="command">
                    <div class="command-name">代码执行</div>
                    <div class="command-desc">编写并运行代码</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🛠️ 工具功能</div>
            <div class="commands">
                <div class="command">
                    <div class="command-name">音乐搜索</div>
                    <div class="command-desc">搜索并获取音乐</div>
                </div>
                <div class="command">
                    <div class="command-name">GitHub 趋势</div>
                    <div class="command-desc">查看 GitHub 热门项目</div>
                </div>
                <div class="command">
                    <div class="command-name">新闻获取</div>
                    <div class="command-desc">获取最新新闻资讯</div>
                </div>
                <div class="command">
                    <div class="command-name">备忘录</div>
                    <div class="command-desc">记录和查询备忘事项</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">👑 管理功能 <span class="tag tag-admin">管理员</span></div>
            <div class="commands">
                <div class="command">
                    <div class="command-name">敏感词管理</div>
                    <div class="command-desc">添加/删除/查看敏感词</div>
                </div>
                <div class="command">
                    <div class="command-name">群组管理</div>
                    <div class="command-desc">禁言/踢人/设置头衔等</div>
                </div>
                <div class="command">
                    <div class="command-name">机器人控制</div>
                    <div class="command-desc">开关机器人、切换模型等</div>
                </div>
                <div class="command">
                    <div class="command-name">管理员列表 <span class="tag tag-super">超管</span></div>
                    <div class="command-desc">添加/移除管理员</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🎮 仙途游戏</div>
            <div class="commands">
                <div class="command">
                    <div class="command-name">游戏介绍</div>
                    <div class="command-desc">了解仙途游戏玩法</div>
                </div>
                <div class="command">
                    <div class="command-name">配置教程</div>
                    <div class="command-desc">SillyTavern/API 配置指南</div>
                </div>
                <div class="command">
                    <div class="command-name">常见问题</div>
                    <div class="command-desc">解答配置和游戏疑问</div>
                </div>
                <div class="command">
                    <div class="command-name">更新日志</div>
                    <div class="command-desc">查看游戏最新更新</div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>💡 提示：直接用自然语言描述你的需求即可</p>
            <p>例如："帮我画一只猫" "今天北京天气怎么样" "搜索一下最新的AI新闻"</p>
        </div>
    </div>
</body>
</html>
'''


def generate_menu_text() -> str:
    """生成文本版菜单"""
    return '''
╔══════════════════════════════════════╗
║        🤖 机器人功能菜单              ║
╠══════════════════════════════════════╣
║                                      ║
║  💬 基础功能                          ║
║  ├─ 智能对话 - @机器人 进行对话        ║
║  ├─ 网络搜索 - 搜索最新信息           ║
║  ├─ 天气查询 - 查询城市天气           ║
║  └─ 网页阅读 - 获取网页内容           ║
║                                      ║
║  🎨 创作功能                          ║
║  ├─ AI 绘画 - 根据描述生成图片        ║
║  ├─ 语音合成 - 文字转语音             ║
║  ├─ 视频生成 - 生成短视频             ║
║  └─ 代码执行 - 编写运行代码           ║
║                                      ║
║  🛠️ 工具功能                          ║
║  ├─ 音乐搜索 - 搜索获取音乐           ║
║  ├─ GitHub 趋势 - 热门项目            ║
║  ├─ 新闻获取 - 最新资讯               ║
║  └─ 备忘录 - 记录事项                 ║
║                                      ║
║  👑 管理功能 [管理员]                  ║
║  ├─ 敏感词管理 - 添加/删除敏感词      ║
║  ├─ 群组管理 - 禁言/踢人/头衔         ║
║  ├─ 机器人控制 - 开关/切换模型        ║
║  └─ 管理员列表 - 添加/移除管理员 [超管]║
║                                      ║
║  🎮 仙途游戏                          ║
║  ├─ 游戏介绍 - 了解游戏玩法           ║
║  ├─ 配置教程 - SillyTavern/API配置   ║
║  ├─ 常见问题 - 解答疑问               ║
║  └─ 更新日志 - 查看最新更新           ║
║                                      ║
╠══════════════════════════════════════╣
║  💡 直接用自然语言描述需求即可         ║
║  例如: "帮我画一只猫"                 ║
║       "今天北京天气怎么样"            ║
╚══════════════════════════════════════╝
'''


@tool(parse_docstring=True)
def show_menu(format_type: str = "image") -> str:
    """显示功能菜单

    Args:
        format_type: 输出格式 (image-图片版 / text-文本版)
    """
    if format_type == "text":
        return generate_menu_text()

    # 图片版
    if not IMGKIT_AVAILABLE:
        logger.warning("imgkit不可用，返回文本版菜单")
        return generate_menu_text()

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        img_file = MENU_DIR / f"menu_{timestamp}.png"

        # imgkit配置
        options = {
            'format': 'png',
            'width': 800,
            'quality': 100,
            'encoding': 'UTF-8',
            'enable-local-file-access': None,
            'quiet': None
        }

        # HTML转图片
        imgkit.from_string(generate_menu_html(), str(img_file), options=options)

        if img_file.exists():
            return f"[图片]{img_file}"
        else:
            logger.error("菜单图片生成失败")
            return generate_menu_text()

    except Exception as e:
        logger.error(f"生成菜单图片失败: {e}")
        return generate_menu_text()


tools = [show_menu]
