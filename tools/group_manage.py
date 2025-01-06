from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, ActionFailed
from nonebot import get_bot, logger
from langchain_core.tools import tool


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


async def set_group_special_title(group_id: int, user_id: int, special_title: str) -> str:
    """设置群成员专属头衔

    Args:
        group_id (int): 群号
        user_id (int): 用户QQ号
        special_title (str): 要设置的头衔，空字符串表示删除头衔

    Returns:
        str: 操作结果的文本描述
    """
    bot: Bot = get_bot()
    try:
        await bot.set_group_special_title(group_id=group_id, user_id=user_id, special_title=special_title)
        return f"已成功{'删除' if not special_title else '设置'}群{group_id}中用户{user_id}的专属头衔{f'为{special_title}' if special_title else ''}"
    except ActionFailed as e:
        logger.error(f"设置群头衔失败: {e.info}")
        return f"设置群头衔失败: {e.info}"


@tool(parse_docstring=True)
async def group_manage(action: str, group_id: int, user_id: int = None, special_title: str = None) -> str:
    """Group management tools
    
    Args:
        action: Operation ("get_info"|"set_title")
        group_id: group_id
        user_id: user_id,设置专属头衔时需要
        special_title: 要设置的专属头衔,设置头衔时需要
    """
    if action == "get_info":
        return await get_group_info(group_id)
    elif action == "set_title":
        if not user_id:
            return "设置专属头衔需要提供用户QQ号"
        return await set_group_special_title(group_id, user_id, special_title or "")
    else:
        return f"不支持的操作类型: {action}"
    
tools = [group_manage]