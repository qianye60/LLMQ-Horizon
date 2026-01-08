"""
机器人管理工具 - 通过自然语言管理机器人
支持的操作：
- 切换模型
- 开关机器人
- 清理会话
- 切换群聊隔离
- 切换分段发送
- 查看状态
- 重载配置
"""
from nonebot import logger
from langchain_core.tools import tool
from .config import config

bot_manage_config = config.get('bot_manage', {})


def get_plugin_config():
    """动态获取插件配置（避免循环导入）"""
    from plugins.llm_chat.config import plugin_config
    return plugin_config


def get_sessions():
    """动态获取会话字典"""
    from plugins.llm_chat import sessions, sessions_lock
    return sessions, sessions_lock


async def get_llm_module():
    """动态获取 LLM 相关模块"""
    from plugins.llm_chat import graph
    from plugins.llm_chat import llm, graph_builder
    return graph, llm, graph_builder


async def check_admin_permission(operator_id: int) -> tuple[bool, str]:
    """检查是否是管理员

    Args:
        operator_id: 操作者 QQ 号

    Returns:
        tuple[bool, str]: (是否有权限, 错误信息)
    """
    plugin_config = get_plugin_config()
    superusers = bot_manage_config.get("superusers", [])

    # 从插件配置中获取超级用户
    plugin_superusers = plugin_config.plugin.superusers
    if plugin_superusers:
        if isinstance(plugin_superusers, str):
            superusers.extend([int(x.strip()) for x in plugin_superusers.split(",") if x.strip().isdigit()])
        elif isinstance(plugin_superusers, list):
            superusers.extend(plugin_superusers)

    if operator_id in superusers:
        return True, ""

    return False, "您不是管理员，无法执行此操作"


async def switch_model(model_name: str) -> str:
    """切换 LLM 模型

    Args:
        model_name: 模型名称
    """
    try:
        import plugins.llm_chat as llm_chat
        from plugins.llm_chat.graph import get_llm, build_graph

        plugin_config = get_plugin_config()

        # 创建新的 LLM 实例
        new_llm = await get_llm(model_name)
        new_graph_builder = await build_graph(plugin_config, new_llm)

        # 更新全局变量
        llm_chat.llm = new_llm
        llm_chat.graph_builder = new_graph_builder

        # 清理所有会话
        sessions, sessions_lock = get_sessions()
        async with sessions_lock:
            sessions.clear()

        logger.info(f"模型已切换到: {model_name}")
        return f"已成功切换到模型: {model_name}，所有会话已清理"
    except Exception as e:
        logger.error(f"切换模型失败: {e}")
        return f"切换模型失败: {str(e)}"


async def get_current_model() -> str:
    """获取当前使用的模型"""
    try:
        import plugins.llm_chat as llm_chat
        if llm_chat.llm is None:
            return "模型尚未初始化"

        model_name = getattr(llm_chat.llm, 'model_name', None) or getattr(llm_chat.llm, 'model', '未知')
        return f"当前模型: {model_name}"
    except Exception as e:
        return f"获取模型信息失败: {str(e)}"


async def toggle_bot(enable: bool) -> str:
    """开关机器人

    Args:
        enable: True 开启，False 关闭
    """
    try:
        plugin_config = get_plugin_config()
        plugin_config.plugin.enable_private = enable
        plugin_config.plugin.enable_group = enable

        status = "开启" if enable else "关闭"
        logger.info(f"机器人已{status}")
        return f"机器人已{status}"
    except Exception as e:
        return f"操作失败: {str(e)}"


async def clear_sessions(scope: str = "all", group_id: int = None, user_id: int = None) -> str:
    """清理会话

    Args:
        scope: 清理范围 ("all" | "group" | "user" | "current")
        group_id: 群号（scope 为 group 时需要）
        user_id: 用户 QQ 号（scope 为 user 时需要）
    """
    try:
        sessions, sessions_lock = get_sessions()

        async with sessions_lock:
            if scope == "all":
                count = len(sessions)
                sessions.clear()
                return f"已清理所有会话，共 {count} 个"

            elif scope == "group" and group_id:
                keys_to_remove = [k for k in sessions if k.startswith(f"group_{group_id}")]
                for k in keys_to_remove:
                    del sessions[k]
                return f"已清理群 {group_id} 的所有会话，共 {len(keys_to_remove)} 个"

            elif scope == "user" and user_id:
                keys_to_remove = [k for k in sessions if str(user_id) in k]
                for k in keys_to_remove:
                    del sessions[k]
                return f"已清理用户 {user_id} 的所有会话，共 {len(keys_to_remove)} 个"

            elif scope == "current" and group_id and user_id:
                plugin_config = get_plugin_config()
                if plugin_config.plugin.group_chat_isolation:
                    thread_id = f"group_{group_id}_{user_id}"
                else:
                    thread_id = f"group_{group_id}"

                if thread_id in sessions:
                    del sessions[thread_id]
                    return f"已清理当前会话"
                return "当前没有活动会话"

            else:
                return "参数错误，请指定正确的清理范围"

    except Exception as e:
        return f"清理会话失败: {str(e)}"


async def toggle_group_isolation(enable: bool) -> str:
    """切换群聊隔离模式

    Args:
        enable: True 开启隔离（每人独立会话），False 关闭隔离（群共享会话）
    """
    try:
        plugin_config = get_plugin_config()
        plugin_config.plugin.group_chat_isolation = enable

        # 清理所有群聊会话以应用新设置
        sessions, sessions_lock = get_sessions()
        async with sessions_lock:
            keys_to_remove = [k for k in sessions if k.startswith("group_")]
            for k in keys_to_remove:
                del sessions[k]

        status = "开启" if enable else "关闭"
        return f"群聊隔离已{status}（{'每人独立会话' if enable else '群内共享会话'}），已清理相关会话"
    except Exception as e:
        return f"操作失败: {str(e)}"


async def toggle_chunk_send(enable: bool) -> str:
    """切换分段发送

    Args:
        enable: True 开启，False 关闭
    """
    try:
        plugin_config = get_plugin_config()
        plugin_config.plugin.chunk.enable = enable

        status = "开启" if enable else "关闭"
        return f"分段发送已{status}"
    except Exception as e:
        return f"操作失败: {str(e)}"


async def get_bot_status() -> str:
    """获取机器人状态"""
    try:
        plugin_config = get_plugin_config()
        sessions, _ = get_sessions()

        import plugins.llm_chat as llm_chat
        model_name = "未初始化"
        if llm_chat.llm:
            model_name = getattr(llm_chat.llm, 'model_name', None) or getattr(llm_chat.llm, 'model', '未知')

        status_lines = [
            "📊 机器人状态",
            f"├─ 当前模型: {model_name}",
            f"├─ 私聊: {'✅ 开启' if plugin_config.plugin.enable_private else '❌ 关闭'}",
            f"├─ 群聊: {'✅ 开启' if plugin_config.plugin.enable_group else '❌ 关闭'}",
            f"├─ 群聊隔离: {'✅ 开启' if plugin_config.plugin.group_chat_isolation else '❌ 关闭'}",
            f"├─ 分段发送: {'✅ 开启' if plugin_config.plugin.chunk.enable else '❌ 关闭'}",
            f"└─ 活动会话数: {len(sessions)}",
        ]

        return "\n".join(status_lines)
    except Exception as e:
        return f"获取状态失败: {str(e)}"


async def set_temperature(temperature: float) -> str:
    """设置模型温度参数

    Args:
        temperature: 温度值 (0.0-2.0)
    """
    try:
        if not 0.0 <= temperature <= 2.0:
            return "温度值必须在 0.0 到 2.0 之间"

        plugin_config = get_plugin_config()
        plugin_config.llm.temperature = temperature

        return f"模型温度已设置为: {temperature}"
    except Exception as e:
        return f"设置失败: {str(e)}"


async def toggle_private_chat(enable: bool) -> str:
    """开关私聊功能"""
    try:
        plugin_config = get_plugin_config()
        plugin_config.plugin.enable_private = enable

        status = "开启" if enable else "关闭"
        return f"私聊功能已{status}"
    except Exception as e:
        return f"操作失败: {str(e)}"


async def toggle_group_chat(enable: bool) -> str:
    """开关群聊功能"""
    try:
        plugin_config = get_plugin_config()
        plugin_config.plugin.enable_group = enable

        status = "开启" if enable else "关闭"
        return f"群聊功能已{status}"
    except Exception as e:
        return f"操作失败: {str(e)}"


@tool(parse_docstring=True)
async def bot_manage(
    action: str,
    operator_id: int,
    model_name: str = None,
    enable: bool = None,
    scope: str = "all",
    group_id: int = None,
    user_id: int = None,
    temperature: float = None
) -> str:
    """机器人管理工具 - 管理员通过自然语言控制机器人

    Args:
        action: 操作类型，可选值：
            - "switch_model": 切换模型
            - "get_model": 获取当前模型
            - "bot_on": 开启机器人
            - "bot_off": 关闭机器人
            - "clear_sessions": 清理会话
            - "isolation_on": 开启群聊隔离
            - "isolation_off": 关闭群聊隔离
            - "chunk_on": 开启分段发送
            - "chunk_off": 关闭分段发送
            - "status": 查看机器人状态
            - "set_temperature": 设置模型温度
            - "private_on": 开启私聊
            - "private_off": 关闭私聊
            - "group_on": 开启群聊
            - "group_off": 关闭群聊
        operator_id: 操作者的QQ号（用于权限验证）
        model_name: 模型名称（切换模型时需要）
        enable: 开关状态
        scope: 清理会话范围 ("all"|"group"|"user"|"current")
        group_id: 群号
        user_id: 用户QQ号
        temperature: 温度值 (0.0-2.0)

    Returns:
        操作结果信息
    """
    # 权限检查
    has_perm, err_msg = await check_admin_permission(operator_id)
    if not has_perm:
        return err_msg

    action_map = {
        "switch_model": lambda: switch_model(model_name) if model_name else "请指定模型名称",
        "get_model": get_current_model,
        "bot_on": lambda: toggle_bot(True),
        "bot_off": lambda: toggle_bot(False),
        "clear_sessions": lambda: clear_sessions(scope, group_id, user_id),
        "isolation_on": lambda: toggle_group_isolation(True),
        "isolation_off": lambda: toggle_group_isolation(False),
        "chunk_on": lambda: toggle_chunk_send(True),
        "chunk_off": lambda: toggle_chunk_send(False),
        "status": get_bot_status,
        "set_temperature": lambda: set_temperature(temperature) if temperature is not None else "请指定温度值",
        "private_on": lambda: toggle_private_chat(True),
        "private_off": lambda: toggle_private_chat(False),
        "group_on": lambda: toggle_group_chat(True),
        "group_off": lambda: toggle_group_chat(False),
    }

    if action not in action_map:
        return f"不支持的操作: {action}。支持的操作: {', '.join(action_map.keys())}"

    handler = action_map[action]

    # 处理异步和同步函数
    import asyncio
    result = handler()
    if asyncio.iscoroutine(result):
        return await result
    return result


tools = [bot_manage]
