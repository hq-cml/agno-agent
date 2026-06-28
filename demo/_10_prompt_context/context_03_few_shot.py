# demo10_03: Few-shot学习 - 用示例教Agent行为模式
# additional_input: 在system message之后、user message之前插入示例消息
# 效果通常比纯instructions要好，因为LLM善于模仿模式

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent

myModel = create_model()

# ======================== Few-shot示例 ========================
# 场景：让Agent按固定格式输出情感分析结果
# 如果只靠instructions描述格式，LLM可能不严格遵守
# 给几个示例后，LLM会严格模仿输出格式

agent = Agent(
    name="情感分析器",
    model=myModel,
    description="你是一个文本情感分析工具",
    instructions=["按照示例格式输出分析结果"],
    # additional_input:
    #   插入到system和user之间的消息列表（通过Debug查看，确实如此）
    # 用user/assistant交替的方式提供few-shot示例
    additional_input=[
        {"role": "user", "content": "分析：今天天气真好，心情愉快！"},                        #user/assistant交替
        {"role": "assistant", "content": "情感: 积极\n置信度: 0.95\n关键词: 天气好, 心情愉快"},
        {"role": "user", "content": "分析：又加班到深夜，太累了"},
        {"role": "assistant", "content": "情感: 消极\n置信度: 0.88\n关键词: 加班, 深夜, 太累"},
    ],
    debug_mode=True,
)

# 实际提问：Agent会模仿上面的格式输出
agent.print_response("分析：这个周末和朋友去爬山，虽然很累但是很开心")
