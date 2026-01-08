import re
from typing import Optional
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, ActionFailed
from nonebot import get_bot, logger
from langchain_core.tools import tool
from .config import config

group_manage_config = config.get('group_manage', {})


async def get_group_member_list(group_id: int) -> str:
    """获取群成员列表

    Args:
        group_id (int): 群号

    Returns:
        str: 群成员列表信息
    """
    bot: Bot = get_bot()
    try:
        members = await bot.get_group_member_list(group_id=group_id)

        # 按角色分类
        owners = []
        admins = []
        member_count = 0

        for m in members:
            role = m.get("role", "member")
            name = m.get("card") or m.get("nickname", str(m["user_id"]))
            if role == "owner":
                owners.append(f"{name}({m['user_id']})")
            elif role == "admin":
                admins.append(f"{name}({m['user_id']})")
            else:
                member_count += 1

        result = [f"群 {group_id} 成员信息:"]
        result.append(f"总人数: {len(members)}")
        if owners:
            result.append(f"群主: {', '.join(owners)}")
        if admins:
            result.append(f"管理员({len(admins)}): {', '.join(admins)}")
        result.append(f"普通成员: {member_count} 人")

        return "\n".join(result)
    except ActionFailed as e:
        logger.error(f"获取群成员列表失败: {e.info}")
        return f"获取群成员列表失败: {e.info}"


async def kick_group_member(group_id: int, operator_id: int, user_id: int, reject_add: bool = False) -> str:
    """踢出群成员

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号
        user_id (int): 被踢出的用户QQ号
        reject_add (bool): 是否拒绝再次加群，默认False
    """
    bot: Bot = get_bot()
    try:
        # 检查权限
        has_perm, err_msg = await check_permission(group_id, operator_id, user_id)
        if not has_perm:
            return err_msg

        await bot.set_group_kick(group_id=group_id, user_id=user_id, reject_add_request=reject_add)
        return f"已将用户 {user_id} 踢出群 {group_id}" + ("，并拒绝再次加群" if reject_add else "")
    except ActionFailed as e:
        logger.error(f"踢人失败: {e.info}")
        return f"踢人失败: {e.info}"


async def set_group_whole_ban(group_id: int, operator_id: int, enable: bool = True) -> str:
    """全员禁言/解除全员禁言

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号
        enable (bool): True开启全员禁言，False关闭
    """
    bot: Bot = get_bot()
    bot_id = int(bot.self_id)

    try:
        # 检查操作者是否有权限
        if operator_id not in group_manage_config.get("superusers", []):
            operator_info = await bot.get_group_member_info(group_id=group_id, user_id=operator_id)
            if operator_info["role"] == "member":
                return "您不是群管理员，无法执行此操作"

        # 检查机器人是否是管理员
        bot_info = await bot.get_group_member_info(group_id=group_id, user_id=bot_id)
        if bot_info["role"] == "member":
            return "机器人不是群管理员，无法执行此操作"

        await bot.set_group_whole_ban(group_id=group_id, enable=enable)
        return f"已{'开启' if enable else '关闭'}群 {group_id} 的全员禁言"
    except ActionFailed as e:
        logger.error(f"设置全员禁言失败: {e.info}")
        return f"设置全员禁言失败: {e.info}"


async def set_group_admin(group_id: int, operator_id: int, user_id: int, enable: bool = True) -> str:
    """设置/取消群管理员

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号（必须是群主）
        user_id (int): 目标用户QQ号
        enable (bool): True设置为管理员，False取消管理员
    """
    bot: Bot = get_bot()
    try:
        # 检查操作者是否是群主或超级用户
        if operator_id not in group_manage_config.get("superusers", []):
            operator_info = await bot.get_group_member_info(group_id=group_id, user_id=operator_id)
            if operator_info["role"] != "owner":
                return "只有群主才能设置管理员"

        await bot.set_group_admin(group_id=group_id, user_id=user_id, enable=enable)
        return f"已{'设置' if enable else '取消'}用户 {user_id} 为群 {group_id} 的管理员"
    except ActionFailed as e:
        logger.error(f"设置管理员失败: {e.info}")
        return f"设置管理员失败: {e.info}"


async def set_group_card(group_id: int, operator_id: int, user_id: int, card: str = "") -> str:
    """设置群名片

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号
        user_id (int): 目标用户QQ号
        card (str): 群名片内容，空字符串表示删除群名片
    """
    bot: Bot = get_bot()
    try:
        # 检查权限（管理员可以改别人，普通成员只能改自己）
        if operator_id != user_id:
            has_perm, err_msg = await check_permission(group_id, operator_id, user_id)
            if not has_perm:
                return err_msg

        await bot.set_group_card(group_id=group_id, user_id=user_id, card=card)
        if card:
            return f"已将用户 {user_id} 在群 {group_id} 的群名片设置为: {card}"
        else:
            return f"已删除用户 {user_id} 在群 {group_id} 的群名片"
    except ActionFailed as e:
        logger.error(f"设置群名片失败: {e.info}")
        return f"设置群名片失败: {e.info}"


async def set_group_name(group_id: int, operator_id: int, group_name: str) -> str:
    """修改群名称

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号
        group_name (str): 新群名称
    """
    bot: Bot = get_bot()
    bot_id = int(bot.self_id)

    try:
        # 检查权限
        if operator_id not in group_manage_config.get("superusers", []):
            operator_info = await bot.get_group_member_info(group_id=group_id, user_id=operator_id)
            if operator_info["role"] == "member":
                return "您不是群管理员，无法修改群名称"

        # 检查机器人权限
        bot_info = await bot.get_group_member_info(group_id=group_id, user_id=bot_id)
        if bot_info["role"] == "member":
            return "机器人不是群管理员，无法修改群名称"

        await bot.set_group_name(group_id=group_id, group_name=group_name)
        return f"已将群 {group_id} 的名称修改为: {group_name}"
    except ActionFailed as e:
        logger.error(f"修改群名称失败: {e.info}")
        return f"修改群名称失败: {e.info}"


async def leave_group(group_id: int, operator_id: int, is_dismiss: bool = False) -> str:
    """退出群聊

    Args:
        group_id (int): 群号
        operator_id (int): 操作者QQ号
        is_dismiss (bool): 是否解散群（仅群主可用）
    """
    bot: Bot = get_bot()
    try:
        # 只有超级用户可以让机器人退群
        if operator_id not in group_manage_config.get("superusers", []):
            return "只有超级管理员才能让机器人退群"

        await bot.set_group_leave(group_id=group_id, is_dismiss=is_dismiss)
        return f"已{'解散' if is_dismiss else '退出'}群 {group_id}"
    except ActionFailed as e:
        logger.error(f"退群失败: {e.info}")
        return f"退群失败: {e.info}"


async def get_group_member_info(group_id: int, user_id: int) -> str:
    """获取群成员详细信息

    Args:
        group_id (int): 群号
        user_id (int): 用户QQ号
    """
    bot: Bot = get_bot()
    try:
        info = await bot.get_group_member_info(group_id=group_id, user_id=user_id, no_cache=True)

        role_map = {"owner": "群主", "admin": "管理员", "member": "成员"}
        role = role_map.get(info.get("role", "member"), "成员")

        result = [
            f"👤 群成员信息",
            f"├─ QQ号: {info['user_id']}",
            f"├─ 昵称: {info.get('nickname', '未知')}",
            f"├─ 群名片: {info.get('card', '无') or '无'}",
            f"├─ 身份: {role}",
            f"├─ 头衔: {info.get('title', '无') or '无'}",
            f"├─ 入群时间: {info.get('join_time', '未知')}",
            f"└─ 最后发言: {info.get('last_sent_time', '未知')}",
        ]

        return "\n".join(result)
    except ActionFailed as e:
        logger.error(f"获取群成员信息失败: {e.info}")
        return f"获取群成员信息失败: {e.info}"


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
async def group_manage(
    action: str,
    group_id: int,
    operator_id: int,
    user_id: int = None,
    special_title: str = None,
    duration: str = "5m",
    card: str = None,
    group_name: str = None,
    enable: bool = True,
    reject_add: bool = False
) -> str:
    """群组管理工具 - 通过自然语言管理群组

    Args:
        action: 操作类型，可选值为 get_info(获取群信息)、get_members(获取群成员列表)、get_member_info(获取群成员详细信息)、set_title(设置群成员专属头衔)、ban(禁言群成员)、unban(解除禁言)、kick(踢出群成员)、whole_ban(全员禁言)、whole_unban(解除全员禁言)、set_admin(设置管理员)、unset_admin(取消管理员)、set_card(设置群名片)、set_group_name(修改群名称)、leave(机器人退群)
        group_id: 群号
        operator_id: 操作者的QQ号（用于权限验证）
        user_id: 目标用户QQ号（部分操作需要）
        special_title: 专属头衔（set_title操作需要）
        duration: 禁言时长，支持格式为纯数字秒数或1d2h3m格式，默认5分钟
        card: 群名片内容（set_card操作需要）
        group_name: 新群名称（set_group_name操作需要）
        enable: 开关状态（用于set_admin等操作）
        reject_add: 踢人时是否拒绝再次加群

    Returns:
        操作结果信息
    """
    action_handlers = {
        "get_info": lambda: get_group_info(group_id),
        "get_members": lambda: get_group_member_list(group_id),
        "get_member_info": lambda: get_group_member_info(group_id, user_id) if user_id else "请提供用户QQ号",
        "set_title": lambda: set_group_special_title(group_id, operator_id, user_id, special_title or "") if user_id else "请提供用户QQ号",
        "ban": lambda: ban_group_member(group_id, operator_id, user_id, duration) if user_id else "请提供用户QQ号",
        "unban": lambda: ban_group_member(group_id, operator_id, user_id, "0") if user_id else "请提供用户QQ号",
        "kick": lambda: kick_group_member(group_id, operator_id, user_id, reject_add) if user_id else "请提供用户QQ号",
        "whole_ban": lambda: set_group_whole_ban(group_id, operator_id, True),
        "whole_unban": lambda: set_group_whole_ban(group_id, operator_id, False),
        "set_admin": lambda: set_group_admin(group_id, operator_id, user_id, True) if user_id else "请提供用户QQ号",
        "unset_admin": lambda: set_group_admin(group_id, operator_id, user_id, False) if user_id else "请提供用户QQ号",
        "set_card": lambda: set_group_card(group_id, operator_id, user_id, card or "") if user_id else "请提供用户QQ号",
        "set_group_name": lambda: set_group_name(group_id, operator_id, group_name) if group_name else "请提供新群名称",
        "leave": lambda: leave_group(group_id, operator_id),
    }

    if action not in action_handlers:
        return f"不支持的操作: {action}。支持的操作: {', '.join(action_handlers.keys())}"

    handler = action_handlers[action]

    import asyncio
    result = handler()
    if asyncio.iscoroutine(result):
        return await result
    return result
    
tools = [group_manage]