# demo07_07: Session State - 多步骤step之间的数据共享
# Input/Output是串行传递（A的输出->B的输入），Session State则是全局共享的"黑板"
# 任何步骤都可以读写Session State，适合跨步骤共享累积数据
# session_state存储在workflow_session.session_data["session_state"]中
# why 这个session_state是如何与db关联的

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

#import sqlite3 实际加载 pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.db.sqlite import SqliteDb
from agno.workflow import Workflow, StepInput, StepOutput
from agno.workflow.step import Step

myModel = create_model()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_state.db")
myDb = SqliteDb(db_file=DB_PATH)


# ======================== 辅助函数：读写session_state ========================
def get_state(step_input: StepInput) -> dict:
    """从StepInput中获取session_state字典"""
    session = step_input.workflow_session
    if session and session.session_data:
        return session.session_data.get("session_state", {})
    return {}

def set_state(step_input: StepInput, key: str, value):
    """向session_state写入数据"""
    session = step_input.workflow_session
    if session:
        if session.session_data is None:
            session.session_data = {}
        if "session_state" not in session.session_data:
            session.session_data["session_state"] = {}
        session.session_data["session_state"][key] = value


# ======================== 用Function执行器演示Session State ========================

# 第1步：收集用户信息，写入session_state
def collect_info(step_input: StepInput) -> StepOutput:
    """从输入中提取信息并存入session_state"""
    user_input = step_input.input or ""
    set_state(step_input, "raw_input", user_input)
    set_state(step_input, "step_count", 1)
    return StepOutput(content=f"已收集输入: {user_input}")


# 第2步：处理数据，读取并更新session_state
def process_data(step_input: StepInput) -> StepOutput:
    """读取session_state中的数据进行处理"""
    state = get_state(step_input)
    raw = state.get("raw_input", "")
    count = state.get("step_count", 0)
    set_state(step_input, "step_count", count + 1)
    set_state(step_input, "processed", True)
    return StepOutput(content=f"已处理数据(第{count+1}步): '{raw}' -> 长度={len(raw)}")


# 第3步：生成报告，读取session_state汇总
def generate_report(step_input: StepInput) -> StepOutput:
    """读取session_state生成最终报告"""
    state = get_state(step_input)
    report = (
        f"=== 执行报告 ===\n"
        f"原始输入: {state.get('raw_input', 'N/A')}\n"
        f"总步骤数: {state.get('step_count', 0) + 1}\n"
        f"已处理: {state.get('processed', False)}\n"
    )
    return StepOutput(content=report)


# ======================== 组装Workflow ========================
workflow = Workflow(
    name="Session State Demo",
    db=myDb,  # 提供db才能持久化session_state
    steps=[
        Step(name="collect", executor=collect_info),
        Step(name="process", executor=process_data),
        Step(name="report", executor=generate_report),
    ],
    # 可以预设初始session_state
    session_state={"version": "1.0"},
)

workflow.print_response("Hello, 这是一条测试消息！")
