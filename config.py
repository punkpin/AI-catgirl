import os

# API设置
API_SETTINGS = {
    "url": "https://api.deepseek.com/v1/chat/completions",
    "model": "deepseek-chat",
    "max_tokens": 1024,
    "frequency_penalty": 0.2
}

# 角色目录
ROLES_DIR = os.path.join(os.path.dirname(__file__), "roles")

# 默认角色
DEFAULT_ROLE = "catgirl"

# 确保角色目录存在
if not os.path.exists(ROLES_DIR):
    os.makedirs(ROLES_DIR)
    print(f"📁 已创建角色目录: {ROLES_DIR}")