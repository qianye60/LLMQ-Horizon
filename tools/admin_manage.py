"""
管理员管理工具 - 通过自然语言管理管理员和敏感词
"""
from langchain_core.tools import tool
from nonebot import logger
from .admin_system import admin_manager, sensitive_words_manager


@tool(parse_docstring=True)
async def admin_manage(
    action: str,
    operator_id: int,
    target_id: int = None,
    word: str = None,
    threshold: int = None,
    duration: int = None,
    enable: bool = None
) -> str:
    """管理员和敏感词管理工具

    Args:
        action: 操作类型，可选值为 set_super(设置超级管理员)、add_admin(添加管理员)、remove_admin(移除管理员)、list_admins(查看管理员列表)、check_permission(检查用户权限)、add_word(添加敏感词)、remove_word(移除敏感词)、list_words(查看敏感词列表和设置)、clear_words(清空敏感词)、set_threshold(设置禁言阈值)、set_duration(设置禁言时长)、toggle_monitor(开关敏感词监控)、toggle_auto_ban(开关自动禁言)、check_violations(查看用户违规次数)、reset_violations(重置用户违规次数)、clear_violations(清空所有违规记录)
        operator_id: 操作者的QQ号（用于权限验证）
        target_id: 目标用户QQ号（用于管理员操作或查看违规）
        word: 敏感词内容
        threshold: 禁言阈值（次数）
        duration: 禁言时长（分钟）
        enable: 开关状态（用于toggle操作）

    Returns:
        操作结果信息
    """
    # 设置超级管理员
    if action == "set_super":
        if target_id is None:
            return "请提供要设置为超级管理员的QQ号"
        success, msg = admin_manager.set_super_admin(target_id, operator_id)
        return msg

    # 添加管理员
    elif action == "add_admin":
        if target_id is None:
            return "请提供要添加的管理员QQ号"
        success, msg = admin_manager.add_admin(target_id, operator_id)
        return msg

    # 移除管理员
    elif action == "remove_admin":
        if target_id is None:
            return "请提供要移除的管理员QQ号"
        success, msg = admin_manager.remove_admin(target_id, operator_id)
        return msg

    # 查看管理员列表
    elif action == "list_admins":
        return admin_manager.get_admin_list()

    # 检查用户权限
    elif action == "check_permission":
        check_id = target_id or operator_id
        if admin_manager.is_super_admin(check_id):
            return f"{check_id} 是超级管理员"
        elif admin_manager.is_admin(check_id):
            return f"{check_id} 是管理员"
        else:
            return f"{check_id} 是普通用户"

    # 添加敏感词（管理员可用）
    elif action == "add_word":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能添加敏感词"
        if not word:
            return "请提供要添加的敏感词"
        success, msg = sensitive_words_manager.add_word(word)
        return msg

    # 移除敏感词（管理员可用）
    elif action == "remove_word":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能移除敏感词"
        if not word:
            return "请提供要移除的敏感词"
        success, msg = sensitive_words_manager.remove_word(word)
        return msg

    # 查看敏感词列表
    elif action == "list_words":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能查看敏感词列表"
        return sensitive_words_manager.get_words_list()

    # 清空敏感词（仅超级管理员可用）
    elif action == "clear_words":
        if not admin_manager.is_super_admin(operator_id):
            return "只有超级管理员才能清空敏感词"
        success, msg = sensitive_words_manager.clear_words()
        return msg

    # 设置禁言阈值
    elif action == "set_threshold":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能设置禁言阈值"
        if threshold is None:
            return "请提供禁言阈值（触发多少次后禁言）"
        success, msg = sensitive_words_manager.set_threshold(threshold)
        return msg

    # 设置禁言时长
    elif action == "set_duration":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能设置禁言时长"
        if duration is None:
            return "请提供禁言时长（分钟）"
        success, msg = sensitive_words_manager.set_ban_duration(duration * 60)
        return msg

    # 开关敏感词监控
    elif action == "toggle_monitor":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能开关敏感词监控"
        if enable is None:
            # 如果没指定，返回当前状态
            status = "开启" if sensitive_words_manager.is_enabled else "关闭"
            return f"敏感词监控当前状态: {status}"
        success, msg = sensitive_words_manager.toggle_enabled(enable)
        return msg

    # 开关自动禁言
    elif action == "toggle_auto_ban":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能开关自动禁言"
        if enable is None:
            # 如果没指定，返回当前状态
            status = "开启" if sensitive_words_manager.is_auto_ban_enabled else "关闭"
            return f"自动禁言当前状态: {status}"
        success, msg = sensitive_words_manager.toggle_auto_ban(enable)
        return msg

    # 查看用户违规次数
    elif action == "check_violations":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能查看违规记录"
        check_id = target_id or operator_id
        count = sensitive_words_manager.get_user_violations(check_id)
        threshold = sensitive_words_manager._data.get("ban_threshold", 3)
        return f"用户 {check_id} 当前违规次数: {count}/{threshold}"

    # 重置用户违规次数
    elif action == "reset_violations":
        if not admin_manager.is_admin(operator_id):
            return "只有管理员才能重置违规记录"
        if target_id is None:
            return "请提供要重置的用户QQ号"
        success, msg = sensitive_words_manager.reset_user_violations(target_id)
        return msg

    # 清空所有违规记录
    elif action == "clear_violations":
        if not admin_manager.is_super_admin(operator_id):
            return "只有超级管理员才能清空所有违规记录"
        success, msg = sensitive_words_manager.clear_all_violations()
        return msg

    else:
        return f"不支持的操作: {action}"


tools = [admin_manage]
