# Team: 高级选项

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model
from agno.agent import Agent
from agno.team import Team, TeamMode

myModel = create_model()

# 成员1：
explore_agent = Agent(
    name="explorer",
    model=myModel,
    role = """搜索网络信息""", # Leader通过这个字段进行分工
)

# 成员2：
research_agent = Agent(
    name="researcher",
    model=myModel,
    role = """深入分析研究""",
)

# 组队
team = Team(
    name="team01",
    model=myModel,
    members=[explore_agent, research_agent], # 这里除了Agent，也可以填另一个Team，从而形成Team嵌套
    description="先搜索信息，再分析整理",
    #debug_mode=True,

    # 四种模式
    mode=TeamMode.coordinate,
    # mode=TeamMode.route,
    # mode=TeamMode.broadcast,
    # mode=TeamMode.tasks,

    # 打印member的数据，便于调试
    show_members_responses=True,

    # 最大迭代（重试）次数
    max_iterations=10,
)

# ret = team.run("分析一下黄大炜的最新信息")
# print(f"\n回复：{ret.content}\n")

#team.print_response("为什么百度不行了", stream=True)
team.print_response("为什么百度不行了")