# demo07_01: 工作流基础 - Step的3种执行器类型
# Step是工作流的最小执行单元，每个Step只绑定一个执行器
# 执行器有3种：Agent、Team、Function

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.team import Team
from agno.workflow import Workflow, StepInput, StepOutput
from agno.workflow.step import Step

myModel = create_model()

# ======================== 执行器类型1：Agent ========================
# 让一个Agent完成某个步骤的任务
researcher = Agent(
    name="researcher",
    model=myModel,
    description="你是一个研究员，负责对给定主题进行简要分析",
    instructions=["用2-3句话总结要点"],
)

research_step = Step(
    name="research",
    agent=researcher,
    description="研究给定主题",
)


# ======================== 执行器类型2：Team ========================
# 让一个Team协作完成某个步骤
explorer = Agent(name="explorer", model=myModel, role="搜索信息")
analyst = Agent(name="analyst", model=myModel, role="分析总结")

research_team = Team(
    name="research_team",
    model=myModel,
    members=[explorer, analyst],
    description="先搜索再分析",
)

analysis_step = Step(
    name="analysis",
    team=research_team,
    description="团队协作分析",
)


# ======================== 执行器类型3：Function ========================
# 自定义Python函数作为执行器，适合做数据预处理、格式转换等确定性操作
# 函数签名固定：接收StepInput，返回StepOutput
def preprocess(step_input: StepInput) -> StepOutput:
    raw = step_input.input or "无输入"
    processed = f"[已预处理] {raw}"
    return StepOutput(content=processed)

preprocess_step = Step(
    name="preprocess",
    executor=preprocess,
    description="预处理输入数据",
)


# ======================== 组装Workflow ========================
# steps列表中的Step按顺序执行，前一个的输出自动传给后一个
workflow = Workflow(
    name="Basic Workflow Demo",
    steps=[
        preprocess_step,  # 第1步：函数预处理
        research_step,    # 第2步：Agent研究（接收预处理的输出）
    ],
    debug_mode=True,
)

# 运行
workflow.print_response("Python在AI领域的应用")
