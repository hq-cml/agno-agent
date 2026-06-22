# demo07_04: Parallel并行 - 多个步骤同时执行，汇总后再继续
# 适用于多个独立研究任务可以并行进行的场景

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.workflow import Workflow, StepInput, StepOutput
from agno.workflow.step import Step
from agno.workflow.parallel import Parallel

myModel = create_model()

# ======================== 定义多个并行Agent ========================
# 优势分析Agent
pros_agent = Agent(
    name="pros_analyst",
    model=myModel,
    description="专门分析事物的优势和好处",
    instructions=["列出3个主要优势，每个用1句话说明"],
)

# 劣势分析Agent
cons_agent = Agent(
    name="cons_analyst",
    model=myModel,
    description="专门分析事物的劣势和风险",
    instructions=["列出3个主要劣势或风险，每个用1句话说明"],
)

# 汇总Agent：综合并行结果给出结论
summarizer = Agent(
    name="summarizer",
    model=myModel,
    description="综合分析师，汇总多方观点给出结论",
    instructions=["基于前面的分析，给出一个平衡的结论和建议，100字以内"],
)

# ======================== 组装Workflow ========================
workflow = Workflow(
    name="Parallel Analysis Pipeline",
    steps=[
        # 第1步：优势和劣势并行分析（同时执行，互不等待）
        Parallel(
            Step(name="pros_analysis", agent=pros_agent),
            Step(name="cons_analysis", agent=cons_agent),
            name="parallel_analysis",
        ),
        # 第2步：汇总（等并行步骤全部完成后执行）
        Step(name="summarize", agent=summarizer),
    ],
)

workflow.print_response("大学生毕业后应该先考研还是先工作")
