"""
敏感词监控插件 - 自动撤回群消息中的敏感词
优先级比 LLM 处理高，所有群消息都会被检查
"""
from nonebot import on_message, logger
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Bot,
)
from nonebot.plugin import PluginMetadata
from tools.admin_system import sensitive_words_manager, admin_manager

__plugin_meta__ = PluginMetadata(
    name="敏感词监控",
    description="自动检查群消息中的敏感词并撤回",
    usage="自动运行，无需手动触发",
)


def _is_group_message(event) -> bool:
    """只处理群消息"""
    return isinstance(event, GroupMessageEvent)


# 优先级设为 1，比 llm_chat 的 10 更高（数字越小优先级越高）
# block=False 允许消息继续传递给其他处理器
sensitive_monitor = on_message(rule=_is_group_message, priority=1, block=False)


@sensitive_monitor.handle()
async def handle_sensitive_check(bot: Bot, event: GroupMessageEvent):
    """检查群消息是否包含敏感词"""
    # 检查敏感词监控是否开启
    if not sensitive_words_manager.is_enabled:
        return

    # 获取消息文本
    text = event.get_plaintext()
    if not text:
        return

    user_id = event.user_id
    group_id = event.group_id
    message_id = event.message_id

    # 检查发送者是否是管理员，管理员不受限制
    if admin_manager.is_admin(user_id):
        return

    # 检查消息
    result = sensitive_words_manager.check_message(text, user_id)

    if not result["matched"]:
        return

    logger.info(f"检测到敏感词 '{result['word']}' - 群:{group_id} 用户:{user_id}")

    # 尝试撤回消息
    if result["should_recall"]:
        try:
            await bot.delete_msg(message_id=message_id)
            logger.info(f"已撤回消息 {message_id}")
        except Exception as e:
            logger.warning(f"撤回消息失败: {e}")

    # 检查是否需要禁言（需要同时满足：达到阈值 + 自动禁言开启）
    if result["should_ban"] and sensitive_words_manager.is_auto_ban_enabled:
        try:
            await bot.set_group_ban(
                group_id=group_id,
                user_id=user_id,
                duration=result["ban_duration"]
            )
            ban_minutes = result["ban_duration"] // 60
            logger.info(f"已禁言用户 {user_id} {ban_minutes} 分钟")

            # 发送提示消息
            await bot.send_group_msg(
                group_id=group_id,
                message=f"[CQ:at,qq={user_id}] 因多次触发敏感词，已被禁言 {ban_minutes} 分钟"
            )
        except Exception as e:
            logger.warning(f"禁言失败: {e}")
