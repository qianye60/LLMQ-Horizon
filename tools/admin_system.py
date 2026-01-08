"""
管理员系统 - 超级管理员和管理员权限管理
数据存储使用 JSON 文件持久化
"""
import json
from pathlib import Path
from typing import Optional, List, Set
from datetime import datetime
from nonebot import logger

# 数据文件路径
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

ADMIN_DATA_FILE = DATA_DIR / "admin_data.json"
SENSITIVE_WORDS_FILE = DATA_DIR / "sensitive_words.json"


class AdminManager:
    """管理员管理器"""

    def __init__(self):
        self._data = self._load_data()

    def _load_data(self) -> dict:
        """加载管理员数据"""
        if ADMIN_DATA_FILE.exists():
            try:
                with open(ADMIN_DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载管理员数据失败: {e}")

        # 默认数据结构
        return {
            "super_admin": None,  # 超级管理员 QQ 号（只能有一个）
            "admins": [],  # 管理员列表
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    def _save_data(self):
        """保存管理员数据"""
        self._data["updated_at"] = datetime.now().isoformat()
        try:
            with open(ADMIN_DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存管理员数据失败: {e}")

    @property
    def super_admin(self) -> Optional[int]:
        """获取超级管理员"""
        return self._data.get("super_admin")

    @property
    def admins(self) -> List[int]:
        """获取管理员列表"""
        return self._data.get("admins", [])

    def set_super_admin(self, user_id: int, operator_id: int) -> tuple[bool, str]:
        """设置超级管理员（只能由当前超级管理员或首次设置时使用）

        Args:
            user_id: 要设置为超级管理员的 QQ 号
            operator_id: 操作者 QQ 号
        """
        current_super = self._data.get("super_admin")

        # 首次设置或由当前超级管理员设置
        if current_super is None or current_super == operator_id:
            self._data["super_admin"] = user_id
            # 如果新超管之前是管理员，从管理员列表移除
            if user_id in self._data["admins"]:
                self._data["admins"].remove(user_id)
            self._save_data()
            return True, f"已设置 {user_id} 为超级管理员"

        return False, "只有当前超级管理员才能转让超级管理员权限"

    def add_admin(self, user_id: int, operator_id: int) -> tuple[bool, str]:
        """添加管理员（只有超级管理员可以操作）

        Args:
            user_id: 要添加的管理员 QQ 号
            operator_id: 操作者 QQ 号
        """
        if not self.is_super_admin(operator_id):
            return False, "只有超级管理员才能添加管理员"

        if user_id == self._data.get("super_admin"):
            return False, "超级管理员不需要添加到管理员列表"

        if user_id in self._data["admins"]:
            return False, f"{user_id} 已经是管理员"

        self._data["admins"].append(user_id)
        self._save_data()
        return True, f"已添加 {user_id} 为管理员"

    def remove_admin(self, user_id: int, operator_id: int) -> tuple[bool, str]:
        """移除管理员（只有超级管理员可以操作）

        Args:
            user_id: 要移除的管理员 QQ 号
            operator_id: 操作者 QQ 号
        """
        if not self.is_super_admin(operator_id):
            return False, "只有超级管理员才能移除管理员"

        if user_id not in self._data["admins"]:
            return False, f"{user_id} 不是管理员"

        self._data["admins"].remove(user_id)
        self._save_data()
        return True, f"已移除管理员 {user_id}"

    def is_super_admin(self, user_id: int) -> bool:
        """检查是否是超级管理员"""
        return self._data.get("super_admin") == user_id

    def is_admin(self, user_id: int) -> bool:
        """检查是否是管理员（包括超级管理员）"""
        return self.is_super_admin(user_id) or user_id in self._data.get("admins", [])

    def get_admin_list(self) -> str:
        """获取管理员列表信息"""
        super_admin = self._data.get("super_admin")
        admins = self._data.get("admins", [])

        lines = ["👑 管理员列表"]
        lines.append(f"├─ 超级管理员: {super_admin or '未设置'}")
        if admins:
            lines.append(f"└─ 管理员({len(admins)}人): {', '.join(map(str, admins))}")
        else:
            lines.append("└─ 管理员: 暂无")

        return "\n".join(lines)


class SensitiveWordsManager:
    """敏感词管理器

    功能：
    - 敏感词触发后撤回消息
    - 累计触发次数达到阈值后禁言
    """

    def __init__(self):
        self._data = self._load_data()

    def _load_data(self) -> dict:
        """加载敏感词数据"""
        if SENSITIVE_WORDS_FILE.exists():
            try:
                with open(SENSITIVE_WORDS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 兼容旧版本数据结构
                    if "words" not in data:
                        data = self._migrate_old_data(data)
                    return data
            except Exception as e:
                logger.error(f"加载敏感词数据失败: {e}")

        return {
            "enabled": True,  # 敏感词监控总开关
            "auto_ban_enabled": False,  # 自动禁言开关（默认关闭）
            "words": [],  # 敏感词列表
            "ban_threshold": 3,  # 禁言阈值（触发多少次后禁言）
            "ban_duration": 600,  # 禁言时长（秒），默认10分钟
            "user_violations": {},  # 用户违规记录 {user_id: {"count": n, "last_time": timestamp}}
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    def _migrate_old_data(self, old_data: dict) -> dict:
        """迁移旧版本数据"""
        words = []
        for key in ["ban_words", "block_words", "warn_words"]:
            words.extend(old_data.get(key, []))
        return {
            "words": list(set(words)),
            "ban_threshold": 3,
            "ban_duration": 600,
            "user_violations": {},
            "created_at": old_data.get("created_at", datetime.now().isoformat()),
            "updated_at": datetime.now().isoformat()
        }

    def _save_data(self):
        """保存敏感词数据"""
        self._data["updated_at"] = datetime.now().isoformat()
        try:
            with open(SENSITIVE_WORDS_FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存敏感词数据失败: {e}")

    def add_word(self, word: str) -> tuple[bool, str]:
        """添加敏感词"""
        word = word.strip()
        if not word:
            return False, "敏感词不能为空"

        if word in self._data["words"]:
            return False, f"'{word}' 已存在"

        self._data["words"].append(word)
        self._save_data()
        return True, f"已添加敏感词 '{word}'"

    def remove_word(self, word: str) -> tuple[bool, str]:
        """移除敏感词"""
        word = word.strip()
        if word not in self._data["words"]:
            return False, f"'{word}' 不在敏感词列表中"

        self._data["words"].remove(word)
        self._save_data()
        return True, f"已移除敏感词 '{word}'"

    def set_threshold(self, threshold: int) -> tuple[bool, str]:
        """设置禁言阈值"""
        if threshold < 1:
            return False, "阈值必须大于0"
        self._data["ban_threshold"] = threshold
        self._save_data()
        return True, f"已设置禁言阈值为 {threshold} 次"

    def set_ban_duration(self, duration: int) -> tuple[bool, str]:
        """设置禁言时长（秒）"""
        if duration < 60:
            return False, "禁言时长不能少于60秒"
        self._data["ban_duration"] = duration
        self._save_data()
        minutes = duration // 60
        return True, f"已设置禁言时长为 {minutes} 分钟"

    def check_message(self, text: str, user_id: int) -> dict:
        """检查消息是否包含敏感词

        Args:
            text: 消息内容
            user_id: 用户QQ号

        Returns:
            {
                "matched": bool,  # 是否匹配到敏感词
                "word": str,  # 匹配到的敏感词
                "should_recall": bool,  # 是否需要撤回
                "should_ban": bool,  # 是否需要禁言
                "ban_duration": int,  # 禁言时长（秒）
                "violation_count": int,  # 当前违规次数
                "threshold": int  # 禁言阈值
            }
        """
        text_lower = text.lower()
        user_id_str = str(user_id)

        for word in self._data.get("words", []):
            if word.lower() in text_lower:
                # 记录违规
                if user_id_str not in self._data["user_violations"]:
                    self._data["user_violations"][user_id_str] = {
                        "count": 0,
                        "last_time": None
                    }

                self._data["user_violations"][user_id_str]["count"] += 1
                self._data["user_violations"][user_id_str]["last_time"] = datetime.now().isoformat()
                self._save_data()

                count = self._data["user_violations"][user_id_str]["count"]
                threshold = self._data["ban_threshold"]
                should_ban = count >= threshold

                # 如果触发禁言，重置计数
                if should_ban:
                    self._data["user_violations"][user_id_str]["count"] = 0
                    self._save_data()

                return {
                    "matched": True,
                    "word": word,
                    "should_recall": True,  # 始终撤回
                    "should_ban": should_ban,
                    "ban_duration": self._data["ban_duration"],
                    "violation_count": count,
                    "threshold": threshold
                }

        return {
            "matched": False,
            "word": None,
            "should_recall": False,
            "should_ban": False,
            "ban_duration": 0,
            "violation_count": 0,
            "threshold": self._data["ban_threshold"]
        }

    def get_user_violations(self, user_id: int) -> int:
        """获取用户违规次数"""
        return self._data["user_violations"].get(str(user_id), {}).get("count", 0)

    def reset_user_violations(self, user_id: int) -> tuple[bool, str]:
        """重置用户违规次数"""
        user_id_str = str(user_id)
        if user_id_str in self._data["user_violations"]:
            self._data["user_violations"][user_id_str]["count"] = 0
            self._save_data()
            return True, f"已重置用户 {user_id} 的违规次数"
        return False, f"用户 {user_id} 没有违规记录"

    def get_words_list(self) -> str:
        """获取敏感词列表"""
        enabled = self._data.get("enabled", True)
        auto_ban = self._data.get("auto_ban_enabled", False)
        words = self._data.get("words", [])
        threshold = self._data.get("ban_threshold", 3)
        duration = self._data.get("ban_duration", 600)

        lines = ["📝 敏感词设置"]
        lines.append(f"├─ 监控状态: {'开启' if enabled else '关闭'}")
        lines.append(f"├─ 自动禁言: {'开启' if auto_ban else '关闭'}")
        lines.append(f"├─ 禁言阈值: {threshold} 次")
        lines.append(f"├─ 禁言时长: {duration // 60} 分钟")
        lines.append(f"├─ 敏感词数量: {len(words)} 个")
        if words:
            lines.append(f"└─ 敏感词列表: {', '.join(words)}")
        else:
            lines.append("└─ 敏感词列表: 无")

        return "\n".join(lines)

    def toggle_enabled(self, enable: bool) -> tuple[bool, str]:
        """开关敏感词监控"""
        self._data["enabled"] = enable
        self._save_data()
        status = "开启" if enable else "关闭"
        return True, f"敏感词监控已{status}"

    def toggle_auto_ban(self, enable: bool) -> tuple[bool, str]:
        """开关自动禁言"""
        self._data["auto_ban_enabled"] = enable
        self._save_data()
        status = "开启" if enable else "关闭"
        return True, f"自动禁言已{status}"

    @property
    def is_enabled(self) -> bool:
        """检查敏感词监控是否开启"""
        return self._data.get("enabled", True)

    @property
    def is_auto_ban_enabled(self) -> bool:
        """检查自动禁言是否开启"""
        return self._data.get("auto_ban_enabled", False)

    def clear_words(self) -> tuple[bool, str]:
        """清空所有敏感词"""
        self._data["words"] = []
        self._save_data()
        return True, "已清空所有敏感词"

    def clear_all_violations(self) -> tuple[bool, str]:
        """清空所有用户的违规记录"""
        self._data["user_violations"] = {}
        self._save_data()
        return True, "已清空所有用户的违规记录"


# 全局实例
admin_manager = AdminManager()
sensitive_words_manager = SensitiveWordsManager()
