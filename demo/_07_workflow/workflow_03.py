# Condition, 条件分支

from agno.workflow.condition import Condition
from agno.workflow.types import StepInput

#定义评估函数，判断条件，返回 bool
def needs_fact_checking(step_input: StepInput) -> bool:
    summary = step_input.previous_step_content or ""
    fact_indicators = ["study shows", "research indicates", "statistics", "%"]
    return any(indicator in summary.lower() for indicator in fact_indicators)



#使用 Condition
workflow =Workflow(
    name="Fact-Check Pipeline",
    steps=[
        research_step,
        summarize_step,
        Condition(
            name="fact_check_condition",
            description="检查是否需要事实核查",
            evaluator=needs_fact_checking, # 返回 bool 的函数
            steps=[
                fact_check_step,           # True 时执行
            ],
            else_steps=[
                publish_step,              # False 时执行
            ],
        ),
        write_article_step,                # 无论如何都会执行
    ],
)

# 说明：evaluator的两种形式
#1.Python函数(最灵活，推荐)
def my_evaluator(step_input: StepInput) -> bool:
    return "urgent" in (step_input.input or "").lower()

#2.CEL 表达式字符串，也就是一个python代码的字符串(声明式，下集详解)
evaluator='input.contains("urgent")'