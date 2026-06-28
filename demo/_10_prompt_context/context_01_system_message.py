# demo10_01: System Message - Agent的"身份证"
# 展示 description、instructions 以及各种 add_xxx_to_context 开关的效果
# 通过 debug_mode=True 观察实际发送给LLM的完整System Message

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent

myModel = create_model()

# ======================== 基础配置 ========================
agent = Agent(
    name="小助手",
    model=myModel,
    # description: 一句话角色定位，会出现在System Message开头
    description="你是一个专业的Python技术顾问",

    # instructions: 行为指令列表，告诉Agent怎么做
    instructions=[
        "回答简洁，不超过100字",
        "如果不确定，直接说不知道",
        "用中文回答",
    ],

    # 以下开关控制System Message中注入哪些额外信息（按需开启，越多token消耗越大）
    add_datetime_to_context=True,    # 注入当前时间（Agent能感知"现在几点"）
    add_name_to_context=True,        # 注入Agent自己的名字
    # add_location_to_context=True,  # 注入地理位置（需要额外配置）
    # add_memories_to_context=True,  # 注入用户记忆（需要配置memory）
    # add_session_state_to_context=True,  # 注入会话状态
    debug_mode=True,  # 开启后可在日志中看到完整的System Message
)

# 运行后观察DEBUG日志中的 system message 部分
agent.print_response("你是谁？现在几点了？今天适合写代码吗？")
