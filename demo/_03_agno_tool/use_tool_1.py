# demo03_1: 使用工具基础
from agno.agent import Agent
from agno.tools import tool
from agno.tools.baidusearch import BaiduSearchTools # 百度的工具，综合搜索
from agno.tools.yfinance import YFinanceTools

#将项目根目录（当前文件所在目录向上两级）添加到Python模块搜索路径的最前面，确保能优先从该目录导入模块，解create_model决跨目录导入问题。
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

# 准备一个模型
myModel = create_model()

# 注意：@tool和@tool()，是有一定区别的
# @tool：就是传统的装饰器
# @tool()：相当于是先调用 tool()，然后将其返回值作为装饰器使用
#   这意味着，tool()是一个工厂函数，它可以根据入参不同，返回不同的装饰器
#   因为这里是无参的，所以建议直接用@tool而非@tool()

# agno 框架的 tool 通常支持两种用法，让开发者可以灵活配置：
# @tool：快速定义工具，使用默认元数据（函数名、文档字符串等自动提取）。
# @tool(...)：需要自定义工具属性时使用，例如：
# @tool(name="weather", description="获取天气")
# def getWeather(city: str) -> str:
#     ...

# 自定义工具
@tool
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

print(f"\n\n\n-----------------------------\n运行结果如下：\n{ret.content}")
