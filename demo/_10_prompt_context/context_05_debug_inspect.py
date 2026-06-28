# demo10_05: 调试检查 - 查看实际发送给LLM的完整消息
# 通过 agent.run_messages 查看最后一次run实际构建的消息列表
# 这比debug_mode的日志更精确，可以看到每条消息的role和content
# 可以看到最底层的message，对比_01_deepseek/deepseek.py中的代码，就能理解最终到底怎么交互的了

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent

myModel = create_model()

agent = Agent(
    name="检查助手",
    model=myModel,
    description="你是一个测试Agent",
    instructions=["用中文简短回答"],
    add_datetime_to_context=True,
    add_name_to_context=True,
    additional_input=[
        {"role": "user", "content": "1+1等于几？"},
        {"role": "assistant", "content": "2"},
    ],
)

# 运行一次
ret = agent.run(
    "你好",
    dependencies={"env": "test", "version": "1.0"},
)
print(f"\n回复: {ret.content}")


# ======================== 检查实际发送的消息 ========================
# RunOutput.messages 包含本次run实际构建的完整消息列表
print("=" * 60)
print("实际发送给LLM的消息列表：")
print("=" * 60)
if ret.messages:
    for i, msg in enumerate(ret.messages):
        role = msg.role
        content = msg.get_content_string() or ""
        # 截断过长内容便于查看
        display = content[:200] + "..." if len(content) > 200 else content
        print(f"\n[{i}] role={role}")
        print(f"    content: {display}")
    print(f"\n\n总消息数: {len(ret.messages)}")


