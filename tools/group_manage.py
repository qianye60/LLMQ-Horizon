import re
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, ActionFailed
from nonebot import get_bot, logger
from langchain_core.tools import tool
from .config import config

group_manage_config = config.get('group_manage', {})


def parse_duration(duration_str: str) -> int:
    """将时间字符串转换为秒数
    支持格式：
    - 简单数字，表示秒数
    - 带单位格式：1d2h3m 表示1天2小时3分钟
    """
    if not duration_str:
        raise ValueError("时间格式不能为空")
        
    if duration_str.isdigit():
        return int(duration_str)
    
    # 解析带单位的格式 (1d2h3m)
    try:
        total_seconds = 0
        pattern = r'(\d+)([dhm])'
        matches = re.findall(pattern, duration_str.lower())
        if matches:
            for value, unit in matches:
                value = int(value)
                if unit == 'd':
                    total_seconds += value * 86400
                elif unit == 'h':
                    total_seconds += value * 3600
                elif unit == 'm':
                    total_seconds += value * 60
            return total_seconds
    except Exception:
        pass
    
    raise ValueError("无效的时间格式，支持的格式：纯数字秒数、或 1d2h3m 格式（如：1d2h3m 表示1天2小时3分钟）")


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
    if operator_id in group_manage_config.get("superusers", []):
        return True, ""
        
    try:
        # 获取群成员信息
        operator_info = await bot.get_group_member_info(group_id=group_id, user_id=operator_id)
        target_info = await bot.get_group_member_info(group_id=group_id, user_id=target_id)
        bot_info = await bot.get_group_member_info(group_id=group_id, user_id=bot_id)
        
        # 检查机器人是否是管理员
        if bot_info["role"] == "member":
            return False, "机器人不是群管理员，无法执行此操作"
            
        # 获取角色等级 (owner: 3, admin: 2, member: 1)
        role_level = {"owner": 3, "admin": 2, "member": 1}
        operator_level = role_level.get(operator_info["role"], 0)
        target_level = role_level.get(target_info["role"], 0)
        
        # 检查操作权限
        if operator_level <= 1:  # 普通成员
            return False, "您不是群管理员，无法执行此操作"
        if operator_level <= target_level:  # 无法操作同级或更高级别的成员
            return False, "无法对同级或更高级别的成员执行此操作"
            
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


async def ban_group_member(group_id: int, operator_id: int, user_id: int, duration: str = None) -> str:
    """禁言群成员

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号（发送命令的用户）
        user_id (int): 被禁言的用户QQ号
        duration (str): 禁言时长，支持格式：
            - 纯数字：表示秒数
            - 带单位格式：1d2h3m 表示1天2小时3分钟
            - None则使用配置中的默认时长
    """
    bot: Bot = get_bot()
    try:
        # 检查权限
        has_perm, err_msg = await check_permission(group_id, operator_id, user_id)
        if not has_perm:
            return err_msg
            
        # 转换时长
        try:
            duration_seconds = 0
            if duration is not None:
                if duration == "0" or duration == 0:  # 处理解除禁言的情况
                    duration_seconds = 0
                else:
                    duration_seconds = parse_duration(duration)
            else:
                duration_seconds = group_manage_config.get("default_ban_duration", 1800)
        except ValueError as e:
            return f"时长格式错误: {str(e)}"
            
        await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=duration_seconds)
        if duration_seconds == 0:
            return f"已解除群{group_id}中用户{user_id}的禁言"
            
        # 格式化显示时间
        days = duration_seconds // 86400
        hours = (duration_seconds % 86400) // 3600
        minutes = (duration_seconds % 3600) // 60
        time_str = []
        if days: time_str.append(f"{days}天")
        if hours: time_str.append(f"{hours}小时")
        if minutes: time_str.append(f"{minutes}分钟")
        time_display = "".join(time_str) if time_str else "0分钟"
        
        return f"已将群{group_id}中用户{user_id}禁言{time_display}"
    except ActionFailed as e:
        logger.error(f"禁言操作失败: {e.info}")
        return f"禁言操作失败: {e.info}"


@tool(parse_docstring=True)
async def group_manage(action: str, group_id: int, operator_id: int, user_id: int = None, special_title: str = None, duration: str = "5m") -> str:
    """Group management tools
    
    Args:
        action: Operation ("get_info"|"set_title"|"ban"|"unban")
        group_id: group_id
        operator_id: 操作者的id(以谁的id执行操作)
        user_id: 设置专属头衔的用户id或要被禁言的用户id
        special_title: 要设置的专属头衔,设置头衔时需要
        duration: 禁言时长，支持格式：纯数字秒数或1d2h3m格式（如：1d2h3m表示1天2小时3分钟），默认5分钟
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
        return await ban_group_member(group_id, operator_id, user_id, "0")
    else:
        return f"不支持的操作类型: {action}"
    
tools = [group_manage]