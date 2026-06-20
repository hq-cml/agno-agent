#Loop 循环
from agno.workflow import Loop
from agno.workflow import Workflow
from agno.workflow.types import StepOutput

def research_evaluator(outputs: List[StepOutput]) -> bool:
    '''评估研究是否充分'''
    for output in outputs:
        if output.content and len(output.content) > 200:
            return True #内容充分，退出循环
        return False    # 内容不足,继续迭代

workflow = Workflow(
    name="Researh Loop Workflow",steps=[
        Loop(
            name="Research Loop",
            steps=[
                research_hn_step,
                research_web_step
            ],
            end_condition=research_evaluator,  # 退出条件，ture则退出
            max_iterations=3,                  # 安全上限，最大迭代次数防止无限循环
            # forward_iteration_output=False,  # 迭代累计模式，默认False
        ),
        content_step,                          #循环结束后执行
)


# TODO:
# forward_iteration_output=True, 每次迭代会接收上一轮迭代输出，实现累计效果