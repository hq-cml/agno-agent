# demo07_09: WorkflowAgent - 智能工作流代理
# 传统Workflow每次都从头到尾执行所有步骤
# WorkflowAgent可以根据历史记录，智能判断哪些步骤不需要重复执行（但是，个人感觉这违背了工作流初衷）

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

#import sqlite3 实际加载 pysqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.workflow import Workflow, WorkflowAgent
from agno.workflow.step import Step

myModel = create_model()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflow_agent.db")
myDb = SqliteDb(db_file=DB_PATH)

# ======================== 定义步骤Agent ========================
researcher = Agent(
    name="researcher",
    model=myModel,
    description="研究员：搜集主题相关信息",
    instructions=["简要列出3个关键发现"],
)

writer = Agent(
    name="writer",
    model=myModel,
    description="写手：基于研究撰写内容",
    instructions=["基于研究结果写100字摘要"],
)

formatter = Agent(
    name="formatter",
    model=myModel,
    description="排版师：格式化最终输出",
    instructions=["将内容格式化为带标题和要点的结构"],
)


# ======================== 创建WorkflowAgent ========================
# WorkflowAgent本身也是一个Agent，它负责决策"是否需要执行某个步骤"
workflow_agent = WorkflowAgent(
    model=myModel,
    # 参考最近N次运行历史来做决策
    num_history_runs=4,
)


# ======================== 组装Workflow ========================
workflow = Workflow(
    name="Smart Article Generation",
    db=myDb,                    # 需要db来存储历史运行记录
    agent=workflow_agent,       # 赋予工作流"智能跳步"能力
    steps=[
        Step(name="research", agent=researcher),
        Step(name="write", agent=writer),
        Step(name="format", agent=formatter),
    ],
)


first_run = not os.path.exists(DB_PATH)
if first_run:
    # 第1次运行：所有步骤都会执行
    print("=" * 50)
    print("第1次运行（全部执行）")
    print("=" * 50)
    workflow.print_response("量子计算的现状")
else:
    # 第2次运行相似主题：WorkflowAgent可能会跳过已有的研究步骤
    print("\n" + "=" * 50)
    print("第2次运行（智能判断是否跳步）")
    print("=" * 50)
    workflow.print_response("量子计算的最新进展")
