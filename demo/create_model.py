from agno.models.openai.like import OpenAILike
import os

# 准备一个模型
def create_model(name="deepseek-v4-flash"):
    if name == "deepseek-v4-flash":
        return OpenAILike(
            id="deepseek-v4-flash",
            api_key=os.environ.get('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com",
        )
    elif name == "deepseek-v4-pro":
        return OpenAILike(
            id="deepseek-v4-pro",
            api_key=os.environ.get('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com",
        )
    else:
        return OpenAILike(
            id="deepseek-v4-flash",
            api_key=os.environ.get('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com",
        )
