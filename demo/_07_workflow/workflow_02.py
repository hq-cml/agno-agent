# demo07_02: Steps容器 - 将多个Step封装成可复用的子流水线
# Steps的价值：
#   复用（多个Workflow共享）
#   封装（隐藏内部细节）
#   组合（与其他控制流混搭）
# 这个其实就是Workflow嵌套

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.workflow import Workflow
from agno.workflow.step import Step
from agno.workflow.steps import Steps

myModel = create_model()

# 定义3个Agent，分别负责不同阶段
researcher = Agent(
    name="researcher",
    model=myModel,
    description="研究员：对主题进行调研分析",
    instructions=["简要列出3个关键点"],
)

writer = Agent(
    name="writer",
    model=myModel,
    description="写手：基于研究结果撰写文章",
    instructions=["基于前一步的研究内容，写一篇200字左右的短文"],
)

editor = Agent(
    name="editor",
    model=myModel,
    description="编辑：润色文章，改善表达",
    instructions=["对前一步的文章进行润色，使其更加流畅专业"],
)

# ======================== 用Steps封装子流水线 ========================
# 把 研究->写作->编辑 封装成一个整体
article_pipeline = Steps(
    name="article_creation",
    description="完整的文章创作流水线",
    steps=[
        Step(name="research", agent=researcher),
        Step(name="writing", agent=writer),
        Step(name="editing", agent=editor),
    ],
)

# ======================== 在Workflow中使用 ========================
# Steps对外表现为一个步骤，内部按顺序执行3个子步骤
workflow = Workflow(
    name="Article Workflow",
    steps=[article_pipeline], # Workflow嵌套
)

workflow.print_response("远程办公的利与弊")
