# demo07_08: Structured IO - 使用Pydantic模型约束输入输出
# 避免脏数据在流程中传播，每个步骤的输入输出都有严格的类型定义

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.workflow import Workflow, StepInput, StepOutput
from agno.workflow.step import Step

myModel = create_model()


# ======================== 定义结构化Schema ========================

# Workflow级别的输入Schema：约束整个工作流的入口数据
class ArticleRequest(BaseModel):
    """文章创作请求"""
    topic: str = Field(description="文章主题")
    style: str = Field(default="正式", description="写作风格：正式/轻松/学术")
    max_words: int = Field(default=200, description="最大字数")


# ======================== 定义步骤 ========================

# 第1步：解析请求（Function执行器，处理结构化输入）
def parse_request(step_input: StepInput) -> StepOutput:
    """解析结构化输入，转换为Agent可理解的提示"""
    # input_schema验证通过后，step_input.input就是Pydantic对象
    if isinstance(step_input.input, ArticleRequest):
        req = step_input.input
        prompt = f"请用{req.style}风格，写一篇关于'{req.topic}'的文章，不超过{req.max_words}字"
    else:
        prompt = f"请写一篇关于'{step_input.input}'的文章"
    return StepOutput(content=prompt)


# 第2步：Agent写作
writer = Agent(
    name="writer",
    model=myModel,
    description="文章撰写专家",
    instructions=["按照要求撰写文章，注意字数限制"],
)


# ======================== 组装Workflow ========================
workflow = Workflow(
    name="Structured Article Workflow",
    input_schema=ArticleRequest,  # 强制验证输入格式
    steps=[
        Step(name="parse", executor=parse_request),
        Step(name="write", agent=writer),
    ],
)

# 使用结构化输入
request = ArticleRequest(
    topic="人工智能的未来",
    style="轻松",
    max_words=150,
)

workflow.print_response(request) # 源头：从一个格式化数据开始
