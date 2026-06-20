# Early Stopping 提前终止
# 各类门控，检测到危险异常，提前终止流程

def security_gate(step_input: StepInput) -> StepOutput:
    result = step_input.previous_step_content or ""
    if "VULNERABLE" in result.upper():
        return StepOutput(
            content="[ALERT]安全漏洞检测到，部署被阻止。",
            stop=True,
        )
    return StepOutput(content="[OK] 检查通过",stop=False)

workflow = Workflow(
    steps=[
        Step(name='Security Scan', agent=scanner),
        Step(name='Security Gate', executor=security_gate),
        Step(name='Deploy Code', agent=deployer),
    ]
)