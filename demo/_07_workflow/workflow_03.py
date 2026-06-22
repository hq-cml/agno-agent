# demo07_03: Condition条件分支 - 根据运行时结果决定走哪条路
# 类似if/else，evaluator返回True走steps，返回False走else_steps

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.workflow import Workflow, StepInput, StepOutput
from agno.workflow.step import Step
from agno.workflow.condition import Condition

myModel = create_model()

# ======================== 定义Agent ========================
# 内容分析Agent：分析用户输入的内容类型
analyzer = Agent(
    name="analyzer",
    model=myModel,
    description="分析输入内容的类型和特征",
    instructions=["判断内容是技术类还是非技术类，简要说明理由"],
)

# 技术写作Agent
tech_writer = Agent(
    name="tech_writer",
    model=myModel,
    description="技术文档撰写专家",
    instructions=["用专业术语撰写技术说明，100字以内"],
)

# 科普写作Agent
popular_writer = Agent(
    name="popular_writer",
    model=myModel,
    description="科普文章撰写专家",
    instructions=["用通俗易懂的语言解释，100字以内"],
)


# ======================== 定义评估函数 ========================
# evaluator接收StepInput（包含上一步的输出），返回bool
def is_tech_content(step_input: StepInput) -> bool:
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{step_input.previous_step_content}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    """判断内容是否属于技术类"""
    content = step_input.previous_step_content or ""
    tech_keywords = ["代码", "编程", "算法", "api", "框架", "技术", "开发", "python", "java"]
    return any(kw in content.lower() for kw in tech_keywords)


# ======================== 组装Workflow ========================
workflow = Workflow(
    name="Smart Writing Pipeline",
    steps=[
        # 第1步：分析内容
        Step(name="analyze", agent=analyzer),
        # 第2步：条件分支
        Condition(
            name="content_type_check",
            description="根据分析结果选择写作风格",
            evaluator=is_tech_content,
            # evaluator返回True时执行
            steps=[
                Step(name="tech_write", agent=tech_writer),
            ],
            # evaluator返回False时执行
            else_steps=[
                Step(name="popular_write", agent=popular_writer),
            ],
        ),
    ],
)

# 测试：技术话题 -> 走tech_writer分支
print("=" * 50)
print("测试1：技术话题")
print("=" * 50)
workflow.print_response("Python的GIL锁机制")

print("\n" + "=" * 50)
print("测试2：非技术话题")
print("=" * 50)
workflow.print_response("如何培养阅读习惯")
