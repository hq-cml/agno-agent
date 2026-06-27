# demo07_05: Loop循环 - 重复执行直到满足退出条件
# 适用于需要迭代改进的场景，如反复润色文章直到质量达标

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model
from typing import List

from agno.agent import Agent
from agno.workflow import Workflow, Loop, StepInput, StepOutput
from agno.workflow.step import Step

myModel = create_model()

# ======================== 定义Agent ========================
# 写作Agent：输出完整文章（非增量），每轮基于上一轮的完整内容润色扩充
writer = Agent(
    name="writer",
    model=myModel,
    description="写作助手，负责撰写和润色文章",
    instructions=[
        "如果是第一次写，请围绕主题撰写一篇短文",
        "如果收到的是已有文章，请在原文基础上润色扩充，输出完整的新版本",
        "每次输出都是完整文章，不要只输出修改部分",
    ],
)

# 审核Agent：评估文章质量，给出"通过"或"需改进"
reviewer = Agent(
    name="reviewer",
    model=myModel,
    description="文章审核员",
    instructions=[
        "评估文章质量，如果内容充实（超过150字）且逻辑通顺，回复'通过'",
        "否则回复'需改进'并指出不足",
    ],
)


# ======================== 定义退出条件 ========================
# end_condition接收当前这一轮迭代所有Step的输出列表，返回True则退出循环
# 这里每轮有2个Step: [writer输出, reviewer输出]
iteration_count = 0
def review_passed(outputs: List[StepOutput]) -> bool:
    """前1轮强制不通过（确保演示多轮迭代），第2轮起看reviewer结果"""
    global iteration_count
    iteration_count += 1
    print(f"  [第{iteration_count}轮迭代完成]")
    # 前2轮强制继续迭代，不依赖LLM判断
    if iteration_count < 2:
        return False
    # 第3轮起，检查reviewer的输出是否包含"通过"
    if outputs and outputs[-1].content:
        return "通过" in str(outputs[-1].content)
    return False


# ======================== 组装Workflow ========================
workflow = Workflow(
    name="Iterative Writing Workflow",
    steps=[
        Loop(
            name="writing_loop",
            steps=[
                Step(name="write", agent=writer),
                Step(name="review", agent=reviewer),
            ],
            end_condition=review_passed,  # reviewer说"通过"就退出
            max_iterations=5,             # 安全上限，防止无限循环
        ),
    ],
)

workflow.print_response("写一篇关于'早起的好处'的短文")

print("----------------------------------------------------")
print("----------------------------------------------------")
print("----------------------------------------------------")

# ======================== 补充示例：forward_iteration_output=True ========================
# 场景：纯Function执行器没有对话历史，必须用forward_iteration_output在轮次间传递数据
#      上面润色文章的场景虽然也有记忆，但那是依靠的Agent对话历史，对于纯Function需要forward_iteration_output
# 模拟：每轮往列表里追加一个元素，直到累积3个

accumulate_count = 0

def accumulate_item(step_input: StepInput) -> StepOutput:
    """每轮从上一轮结果中取出列表，追加一个新元素"""
    global accumulate_count
    accumulate_count += 1

    # 第1轮时previous_step_content为None，初始化空列表
    prev = step_input.previous_step_content
    if isinstance(prev, str) and prev.startswith("["):
        import ast
        items = ast.literal_eval(prev)
    else:
        items = []

    items.append(f"item_{accumulate_count}")
    print(f"  第{accumulate_count}轮: {items}")
    return StepOutput(content=str(items))


def has_three_items(outputs: List[StepOutput]) -> bool:
    """累积到3个元素就退出"""
    if outputs and outputs[-1].content:
        return "item_3" in str(outputs[-1].content)
    return False


workflow2 = Workflow(
    name="Accumulate Demo",
    steps=[
        Loop(
            name="accumulate_loop",
            steps=[
                Step(
                    name="accumulate",
                    executor=accumulate_item
                ),
            ],
            end_condition=has_three_items,
            max_iterations=5,
            # 关键：开启后每轮的输出会作为下一轮的输入
            # 如果不开启，每轮step_input.previous_step_content都是None，列表永远只有1个元素
            forward_iteration_output=True,
        ),
    ],
)

print("\n\n" + "=" * 50)
print("补充示例：forward_iteration_output=True（纯函数累积）")
print("=" * 50)
workflow2.print_response("开始累积")

#- 第 1 轮：previous_step_content 为空 → 初始化空列表 → 追加 item_1 → 输出 ['item_1']
#- 第 2 轮：因为 forward_iteration_output=True，收到上轮输出 ['item_1'] → 追加 item_2 → 输出 ['item_1', 'item_2']
#- 第 3 轮：收到 ['item_1', 'item_2'] → 追加 item_3 → 退出
#如果把 forward_iteration_output 改成 False，每轮都会从空列表开始，永远只有 1 个