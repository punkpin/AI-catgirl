import os
import json
from config import ROLES_DIR, DEFAULT_ROLE


class RoleManager:
    def __init__(self):
        self.roles = self.load_all_roles()
        self.current_role_name = DEFAULT_ROLE  # 存储当前角色名称
        self.current_role = self.get_role(self.current_role_name)  # 存储当前角色配置

    def load_all_roles(self):
        """加载所有可用角色"""
        roles = {}
        if not os.path.exists(ROLES_DIR):
            print(f"⚠️ 角色目录不存在: {ROLES_DIR}")
            return {DEFAULT_ROLE: self.create_default_role()}

        for filename in os.listdir(ROLES_DIR):
            if filename.endswith(".json"):
                role_name = filename.split(".")[0]  # 从文件名获取角色名
                try:
                    filepath = os.path.join(ROLES_DIR, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        roles[role_name] = json.load(f)
                    print(f"✅ 已加载角色: {role_name}")
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"⚠️ 加载角色 {role_name} 失败: {str(e)}")

        # 确保至少有一个默认角色
        if not roles:
            roles[DEFAULT_ROLE] = self.create_default_role()
            print(f"⚠️ 未找到角色配置，已创建默认角色: {DEFAULT_ROLE}")

        return roles

    def create_default_role(self):
        """创建默认角色配置"""
        return {
            "name": "默认助手",
            "system_prompt": "你是一个乐于助人的AI助手",
            "greeting": "你好！有什么我可以帮助你的吗？",
            "exit_message": "再见！",
            "error_message": "抱歉，出错了",
            "temperature": 0.7
        }

    def get_role(self, role_name):
        """获取指定角色配置"""
        return self.roles.get(role_name, self.roles[DEFAULT_ROLE])

    def list_roles(self):
        """列出所有可用角色"""
        return list(self.roles.keys())

    def set_role(self, role_name):
        """设置当前角色"""
        if role_name in self.roles:
            self.current_role_name = role_name
            self.current_role = self.roles[role_name]
            return True
        return False

    def get_current_role(self):
        """获取当前角色配置"""
        return self.current_role

    def get_current_role_name(self):
        """获取当前角色名称"""
        return self.current_role_name