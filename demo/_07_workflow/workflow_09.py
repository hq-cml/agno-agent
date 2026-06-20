#WorkfllowAgent
#传统的workflow，每次都是从头到尾执行
#workflow_agent可以职能判断哪些步骤不需要重复执行

from agno.workflow import WorkflowAgent
workflow_agent = WorkflowAgent(
    model=OpenAIChat(),
    num_history_runs=4,
)

workflow = Workflow(
    name="Story Generation",
    agent=workflow_agent,
    steps=[writer_step, formatter_step],
)