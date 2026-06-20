# parallel, 并行
from agno.workflow.parallel import Parallel

workflow = Workflow(
    name="Content Creation Pipeline",
    steps=[
        #两个研究步骤并行执行
        Parallel(
            research_hn_step,  #HackerNews 研究
            research_web_step,       #Web 搜索
            name="Research Phase",
        ),
        #并行结束后，顺序执行后续步骤
        write_step,
        review_step,
    ],
)