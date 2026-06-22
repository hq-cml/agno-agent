# demo07_06: Router动态路由 - 根据运行时条件动态选择下一步骤
# 与Condition的区别：Condition是二选一(if/else)，Router可以多选一甚至多选多

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model
from typing import List

from agno.agent import Agent
from agno.workflow import Workflow, StepInput, StepOutput
from agno.workflow.step import Step
from agno.workflow.router import Router

myModel = create_model()

# ======================== 定义多个专业Agent ========================
tech_agent = Agent(
    name="tech_expert",
    model=myModel,
    description="技术领域专家",
    instructions=["从技术角度回答问题，简洁专业"],
)

finance_agent = Agent(
    name="finance_expert",
    model=myModel,
    description="金融领域专家",
    instructions=["从金融角度回答问题，简洁专业"],
)

general_agent = Agent(
    name="general_expert",
    model=myModel,
    description="通用知识专家",
    instructions=["用通俗易懂的方式回答问题"],
)

# 定义Step对象
tech_step = Step(name="tech_answer", agent=tech_agent)
finance_step = Step(name="finance_answer", agent=finance_agent)
general_step = Step(name="general_answer", agent=general_agent)


# ======================== 定义路由选择函数 ========================
# selector接收StepInput，返回要执行的Step列表
# 返回类型可以是：List[Step]、Step、str(步骤名)、List[str]
def topic_router(step_input: StepInput) -> List[Step]:
    """根据输入主题选择对应的专家"""
    topic = (step_input.input or "").lower()

    tech_keywords = ["编程", "代码", "算法", "ai", "python", "软件", "技术"]
    finance_keywords = ["股票", "基金", "投资", "理财", "金融", "经济"]

    if any(kw in topic for kw in tech_keywords):
        return [tech_step]
    elif any(kw in topic for kw in finance_keywords):
        return [finance_step]
    else:
        return [general_step]


# ======================== 组装Workflow ========================
workflow = Workflow(
    name="Smart Router Workflow",
    steps=[
        Router(
            name="topic_router",
            selector=topic_router,
            choices=[tech_step, finance_step, general_step],
        ),
    ],
)

# 测试不同主题的路由
print("=" * 50)
print("测试1：技术话题")
print("=" * 50)
workflow.print_response("Python的异步编程怎么实现")

print("\n" + "=" * 50)
print("测试2：金融话题")
print("=" * 50)
workflow.print_response("新手应该怎么买基金")
