import pprint
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model
from agno.agent import Agent
from agno.team import Team

myModel = create_model()

# 成员1：
explore_agent = Agent(
    name="explorer",
    model=myModel,
    #description="你负责发现新知识，并记录下来",
    role = """搜索网络信息""",
)

# 成员2：
research_agent = Agent(
    name="researcher",
    model=myModel,
    #description="你负责发现新知识，并记录下来",
    role = """深入分析研究""",
)

# 组队
team = Team(
    name="team01",
    model=myModel,
    members=[explore_agent, research_agent],
    description="先搜索信息，再分析整理",
    #debug_mode=True,
)

# ret = team.run("分析一下黄大炜的最新信息")
# print(f"\n回复：{ret.content}\n")

#team.print_response("为什么百度不行了", stream=True)
team.print_response("为什么百度不行了")