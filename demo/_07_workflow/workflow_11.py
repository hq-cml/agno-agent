# demo07_11: Early Stopping提前终止 - 检测到异常时立即中断流程
# 通过StepOutput(stop=True)实现，后续步骤将不再执行
# 典型场景：安全门控、质量检查、异常熔断

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.workflow import Workflow, StepInput, StepOutput
from agno.workflow.step import Step

myModel = create_model()

# ======================== 模拟场景：代码部署流水线 ========================
# 流程：代码扫描 -> 安全门控 -> 部署
# 如果安全扫描发现漏洞，则阻止部署

# 第1步：代码扫描（模拟，实际可以调用扫描工具）
def code_scanner(step_input: StepInput) -> StepOutput:
    """模拟代码安全扫描"""
    code_desc = step_input.input or ""
    # 模拟扫描结果：包含"eval"或"exec"则标记为有漏洞
    if any(danger in code_desc.lower() for danger in ["eval", "exec", "sql注入", "漏洞"]):
        return StepOutput(content="[扫描结果] 发现安全漏洞: VULNERABLE")
    return StepOutput(content="[扫描结果] 代码安全: PASSED")


# 第2步：安全门控（根据扫描结果决定是否继续）
def security_gate(step_input: StepInput) -> StepOutput:
    """安全门控：检测到漏洞则终止整个流程"""
    result = step_input.previous_step_content or ""
    if "VULNERABLE" in result.upper():
        return StepOutput(
            content="[ALERT] 安全漏洞检测到，部署被阻止！请修复后重试。",
            stop=True,  # 关键：stop=True终止后续所有步骤
        )
    return StepOutput(content="[OK] 安全检查通过，继续部署")


# 第3步：部署（只有安全检查通过才会执行）
def deploy(step_input: StepInput) -> StepOutput:
    """模拟部署"""
    return StepOutput(content="[SUCCESS] 代码已成功部署到生产环境！🚀")


# ======================== 组装Workflow ========================
workflow = Workflow(
    name="Deploy Pipeline",
    steps=[
        Step(name="scan", executor=code_scanner),
        Step(name="gate", executor=security_gate),
        Step(name="deploy", executor=deploy),   # stop=True时不会执行到这里
    ],
)

# 测试1：安全的代码
print("=" * 50)
print("测试1：安全代码 -> 正常部署")
print("=" * 50)
workflow.print_response("新增用户注册功能，使用参数化查询")

# 测试2：有漏洞的代码
print("\n" + "=" * 50)
print("测试2：有漏洞代码 -> 阻止部署")
print("=" * 50)
workflow.print_response("使用eval执行用户输入的表达式")
