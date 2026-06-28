# demo10_04: 历史记忆 - 多轮对话的上下文管理
# 展示 add_history_to_context、num_history_runs、max_tool_calls_from_history

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

#import sqlite3 实际加载 pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

myModel = create_model()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history_demo.db")
myDb = SqliteDb(db_file=DB_PATH)

# ======================== 带历史记忆的Agent ========================
agent = Agent(
    name="记忆助手",
    model=myModel,
    description="你是一个有记忆的助手，能记住之前的对话",
    instructions=["简洁回答，50字以内"],
    db=myDb,

    # 历史记忆相关配置
    add_history_to_context=True,   # 开启历史加载
    num_history_runs=3,            # 最多加载最近3轮对话
    # max_tool_calls_from_history=2,  # 历史中最多保留2次tool调用结果（防止窗口爆满）
    debug_mode=True,
)

# 关于SESSION ID的问题
# 它是对话history的抓手（不是user_id，那个只是记忆桶的标识）
# 一轮对话中，如果没有手动指定Session id，那么如果agent实例不重启，会有自动的同一个session id
# 一旦Agent重启了，则session id将丢失，所以要想记忆对话历史，应该指定session id或者不重启agent

SESSION_ID="fixed_session_001"

# 模拟多轮对话
first_run = not os.path.exists(DB_PATH)
if first_run:
    # 第1轮：告诉Agent一些信息
    print("=== 第1轮 ===")
    ret = agent.run(
        "我叫张三，我是一个Python开发者",
        user_id="test_user",
        session_id=SESSION_ID,
    )
    print(f"回复：{ret.content}\n")

    # 第2轮：继续补充
    print("=== 第2轮 ===")
    ret = agent.run(
        "我在北京工作，喜欢爬山",
        user_id="test_user",
        session_id=SESSION_ID,
    )
    print(f"回复：{ret.content}\n")
else:
    # 第3轮：测试Agent是否记住了之前的对话
    print("=== 验证记忆 ===")
    ret = agent.run(
        "我叫什么名字？在哪里工作？",
        user_id="test_user",
        session_id=SESSION_ID,
    )
    print(f"回复：{ret.content}\n")
