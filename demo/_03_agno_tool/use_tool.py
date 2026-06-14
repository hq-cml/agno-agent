# demo03: 使用工具
from agno.agent import Agent
from demo.create_model import create_model
from agno.tools import tool
from agno.tools.baidusearch import BaiduSearchTools # 百度的工具，综合搜索
from agno.tools.yfinance import YFinanceTools
import json

# 准备一个模型
myModel = create_model()

# 自定义工具
@tool()
def myCalc(expression):
    """
    计算一个数学表达式
    """
    print("myCalc工具被使用：----------------------->", expression)
    return eval(expression)

agent = Agent(
    name="agno v0.1",
    model=myModel,
    tools=[
        myCalc,               # 调用自己的工具
        BaiduSearchTools(),   # 通用搜索，对于股价这类高实时性的搜索会有很大延迟
        YFinanceTools(),      # 精确财经搜索，比如搜股价，要求实时性
    ],
    description="你是一个通用Agent，负责回答各类问题。",
    instructions="如果有符合条件的tool，优先使用tool！",
    debug_mode=True,
)


#ret = agent.run("1024*1024=多少？")
#ret = agent.run("腾讯的当前股价是多少？")
#ret = agent.run("歌手黄大炜现状？")
ret = agent.run("歌手黄大炜去世了吗？")

print(f"\n\n\n-----------------------------\n运行结果如下：\n{ret.reasoning_content}")
