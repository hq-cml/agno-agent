# demo07_12: Human in the Loop (HITL) - 关键步骤要求人工确认
# 在敏感操作前暂停流程，等待人工审批后再继续
# 需要db支持（用于持久化暂停状态）

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

#import sqlite3 实际加载 pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.workflow import Workflow, StepInput, StepOutput
from agno.workflow.step import Step
from agno.workflow.types import OnReject

myModel = create_model()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hitl.db")
myDb = SqliteDb(db_file=DB_PATH)

# ======================== 定义步骤 ========================

# 第1步：数据采集（自动执行）
fetch_agent = Agent(
    name="data_fetcher",
    model=myModel,
    description="数据采集Agent",
    instructions=["模拟采集数据，返回采集结果摘要"],
)

# 第2步：数据处理（需要人工确认）
process_agent = Agent(
    name="data_processor",
    model=myModel,
    description="数据处理Agent，处理敏感数据",
    instructions=["对采集到的数据进行处理和分析"],
)

# 第3步：结果输出（自动执行）
def output_result(step_input: StepInput) -> StepOutput:
    return StepOutput(content=f"最终结果: {step_input.previous_step_content}")


# ======================== 组装Workflow ========================
workflow = Workflow(
    name="HITL Demo Workflow",
    db=myDb,  # HITL需要db来持久化暂停状态
    steps=[
        Step(name="fetch_data", agent=fetch_agent),
        Step(                                         # 人工确认，封装在一个完整的step中
            name="process_data",
            agent=process_agent,
            # HITL核心配置
            requires_confirmation=True,                # 执行前需要人工确认
            confirmation_message="即将处理敏感数据，是否确认继续？",
            # on_reject=OnReject.skip,                   # 拒绝时跳过此步骤继续后续流程
            on_reject=OnReject.cancel,                   # 拒绝时取消整个工作流
        ),
        Step(name="output", executor=output_result),
    ],
)

# ======================== 运行演示 ========================
# HITL不能用print_response（它只调一次run就结束了）
# 正确流程：run() -> 检查paused -> 人工决策 -> continue_run()

result = workflow.run("请采集并处理最近一周的用户行为数据")
print(f"第1次run结果: status={result.status}")

# 检查是否暂停等待确认
if result.is_paused:
    print(f"\n⏸️  工作流暂停！")
    for req in result.active_step_requirements:
        if req.needs_confirmation:
            print(f"   步骤 '{req.step_name}' 需要确认")
            print(f"   消息: {req.confirmation_message}")

            # 模拟人工决策（实际场景中这里会等待用户输入）
            user_choice = input("   是否确认？(y/n): ").strip().lower()
            if user_choice == "y":
                req.confirm()
                print("   ✅ 已确认")
            else:
                req.reject()
                print("   ❌ 已拒绝")

    # 恢复执行
    result = workflow.continue_run(result)
    print(f"\n继续执行后: status={result.status}")
    print(f"最终输出: {result.content}")
