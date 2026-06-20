#Router 动态路由

from agno.workflow.router import Router
def research_router(step_input: StepInput) -> List[Step]:
    '''根据主题选择研究策略'''
    topic = step_input.input.lower()
    tech_keywords = ["ai", "programming", "software", "startup"]
    if any(kw in topic for kw in tech_keywords):
        return [research_hackernews] #技术话题 -HN
    return [research_web]            #其他Web搜索

workflow= Workflow(
    name="Intelligent Research Workflow",
    steps=[
    Router(
        name="research_strategy_router",
        selector=research_router,                    # 选择函数
        choices=[research_hackernews,research_web],  # 可选步骤
    ],
)

# TODO selector的四种返回类型