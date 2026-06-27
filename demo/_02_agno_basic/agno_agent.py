# demo02: 基于模型的基础问答机器人
import sys, os
from agno.agent import Agent

#将项目根目录（当前文件所在目录向上两级）添加到Python模块搜索路径的最前面，确保能优先从该目录导入模块，解决create_model跨目录导入问题。
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

# 准备一个模型
myModel = create_model()

# 基于准备好的模型创建一个Agent
# 参数：
#   description：描述 Agent 的身份、角色、背景知识。例子：“你是一位精通Python的编程助手。”
#   instructions：给出具体的行为指令、格式约束、任务步骤。例子：“每次回答必须使用中文。”
#       说明：事实上description和instructions最后都会合并作为system promt，但是他们的定位还是有细微差别的。
#   debug_mode=True：可以看到Agent运行细节日志、token消耗等情况
#   markdown：Agent 生成的回复会包含 Markdown 语法（如 **加粗**等）。如果前端或终端支持 Markdown 渲染
#           （比如在 Jupyter Notebook、支持 Markdown 的聊天界面或某些命令行工具中），这些格式会被正确显示为富文本，提升可读性。
agent = Agent(
    name="agno v0.1",
    model=myModel,
    #description="你是一个测试Agent，负责回答各类问题。要求是必须用中文回复！",
    description="你是一个测试Agent，负责回答各类问题。",
    instructions="无论问题是何种语言，要求是必须用中文回复！",
    markdown=False,
    debug_mode=True,
)

# run运行一个具体任务，不关心输出的时候执行
# print_response通常用于问答，需要明确答案

agent.run("中国是哪一年成立的？")
#agent.run("江苏省淮安市有什么好玩的？")
#agent.print_response("江苏省淮安市有什么好玩的？")
#agent.print_response("who is Albert Einstein?")
#agent.run("who is Albert Einstein?")