from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, ActionFailed
from nonebot import get_bot, logger
from langchain_core.tools import tool
from .config import config

group_manage_config = config.get('group_manage', {})


async def check_permission(group_id: int, operator_id: int, target_id: int) -> tuple[bool, str]:
    """检查权限

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号（发送命令的用户）
        target_id (int): 被操作者QQ号

    Returns:
        tuple[bool, str]: (是否有权限, 错误信息)
    """
    bot: Bot = get_bot()
    bot_id = int(bot.self_id)
    
    # 检查操作者是否是超级用户
    if operator_id not in group_manage_config.get("superusers", []):
        return False, f"发送命令的用户权限不足，不在超级用户列表中，无法执行此操作。"
        
    try:
        # 获取群成员信息
        group_info = await bot.get_group_member_info(group_id=group_id, user_id=target_id)
        bot_info = await bot.get_group_member_info(group_id=group_id, user_id=bot_id)
        
        # 检查机器人是否是管理员
        if bot_info["role"] == "member":
            return False, "机器人不是群管理员，无法执行此操作"
            
        # 检查目标是否是群主或管理员
        if group_info["role"] in ["owner", "admin"]:
            return False, "无法对群主或管理员执行此操作"
            
        return True, ""
    except ActionFailed as e:
        logger.error(f"获取群成员信息失败: {e.info}")
        return False, f"权限检查失败: {e.info}"


async def get_group_info(group_id: int) -> str:
    """获取群信息

    Args:
        group_id (int): 群号

    Returns:
        str: 群信息的文本描述
    """
    bot: Bot = get_bot()
    try:
        group_info = await bot.get_group_info(group_id=group_id, no_cache=True)
        return f"群名称: {group_info['group_name']}\n群号: {group_info['group_id']}\n群人数: {group_info['member_count']}\n群上限: {group_info['max_member_count']}"
    except ActionFailed as e:
        logger.error(f"获取群信息失败: {e.info}")
        return f"获取群信息失败: {e.info}"


async def set_group_special_title(group_id: int, operator_id: int, user_id: int, special_title: str) -> str:
    """设置群成员专属头衔

    Args:
        group_id (int): group_id
        operator_id (int): operator user id (user who sent the command)
        user_id (int): The QQ account to operate on, the QQ ID to be banned
        special_title (str): The title to be set, an empty string indicates that the title should be removed
    """
    bot: Bot = get_bot()
    try:
        # 检查权限
        has_perm, err_msg = await check_permission(group_id, operator_id, user_id)
        if not has_perm:
            return err_msg
            
        await bot.set_group_special_title(group_id=group_id, user_id=user_id, special_title=special_title)
        return f"已成功{'删除' if not special_title else '设置'}群{group_id}中用户{user_id}的专属头衔{f'为{special_title}' if special_title else ''}"
    except ActionFailed as e:
        logger.error(f"设置群头衔失败: {e.info}")
        return f"设置群头衔失败: {e.info}"


async def ban_group_member(group_id: int, operator_id: int, user_id: int, duration: int = None) -> str:
    """禁言群成员

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号（发送命令的用户）
        user_id (int): 被禁言的用户QQ号
        duration (int): 禁言时长(秒)，0表示解除禁言，None则使用配置中的默认时长

    Returns:
        str: 操作结果的文本描述
    """
    bot: Bot = get_bot()
    try:
        # 检查权限
        has_perm, err_msg = await check_permission(group_id, operator_id, user_id)
        if not has_perm:
            return err_msg
            
        # 如果未指定时长，使用配置中的默认时长
        if duration is None:
            duration = group_manage_config.get("default_ban_duration", 1800)
            
        await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=duration)
        if duration == 0:
            return f"已解除群{group_id}中用户{user_id}的禁言"
        return f"已将群{group_id}中用户{user_id}禁言{duration}秒"
    except ActionFailed as e:
        logger.error(f"禁言操作失败: {e.info}")
        return f"禁言操作失败: {e.info}"


@tool(parse_docstring=True)
async def group_manage(action: str, group_id: int, operator_id: int, user_id: int = None, special_title: str = None, duration: int = None) -> str:
    """Group management tools
    
    Args:
        action: Operation ("get_info"|"set_title"|"ban"|"unban")
        group_id: group_id
        operator_id: 操作者QQ号（发送命令的用户）
        user_id: user_id,设置专属头衔或禁言时需要
        special_title: 要设置的专属头衔,设置头衔时需要
        duration: 禁言时长(秒),不指定则使用配置中的默认时长
    """
    if action == "get_info":
        return await get_group_info(group_id)
    elif action == "set_title":
        if not user_id:
            return "设置专属头衔需要提供用户QQ号"
        return await set_group_special_title(group_id, operator_id, user_id, special_title or "")
    elif action == "ban":
        if not user_id:
            return "禁言操作需要提供用户QQ号"
        return await ban_group_member(group_id, operator_id, user_id, duration)
    elif action == "unban":
        if not user_id:
            return "解除禁言需要提供用户QQ号"
        return await ban_group_member(group_id, operator_id, user_id, 0)
    else:
        return f"不支持的操作类型: {action}"
    
tools = [group_manage]