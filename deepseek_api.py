import os
import json
import requests
from dotenv import load_dotenv
from config import API_SETTINGS

# 加载环境变量
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    raise ValueError("❌ 未找到DEEPSEEK_API_KEY环境变量！请在.env文件中添加")


class DeepSeekAPI:
    @staticmethod
    def generate_response(role_config, user_input: str) -> str:
        """获取AI回复"""
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": API_SETTINGS["model"],
            "messages": [
                {
                    "role": "system",
                    "content": role_config["system_prompt"]
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "temperature": role_config.get("temperature", 0.7),
            "max_tokens": API_SETTINGS["max_tokens"],
            "frequency_penalty": API_SETTINGS["frequency_penalty"]
        }

        try:
            response = requests.post(
                API_SETTINGS["url"],
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except requests.exceptions.RequestException as e:
            error_msg = role_config.get("error_message", f"请求出错: {str(e)}")
            return f"❌ {error_msg}"
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            error_msg = role_config.get("error_message", f"解析错误: {str(e)}")
            return f"❌ {error_msg}"