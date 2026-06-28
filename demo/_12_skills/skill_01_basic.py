# demo12_01: Skills基础 - 给Agent加载本地技能
# Skill = SKILL.md(指令) + references/(参考文档) + scripts/(脚本)
# Agent会自动获得3个工具来访问这些技能内容

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent
from agno.skills import Skills
from agno.skills.loaders.local import LocalSkills

myModel = create_model()

# ======================== 加载本地技能 ========================
# 技能目录结构：
#   my_skills/
#     code_review/
#       SKILL.md          <- 技能主文件（frontmatter + 指令）
#       references/       <- 参考文档目录
#         python_style.md
#       scripts/          <- 可执行脚本目录
#         count_lines.py

SKILLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_skills")

skills = Skills(loaders=[LocalSkills(SKILLS_DIR)]) # 加载本地skill

# 查看加载了哪些技能
print("已加载的技能:")
for name in skills.get_skill_names():
    skill = skills.get_skill(name)
    print(f"  - {name}: {skill.description}")
    print(f"    references: {skill.references}")
    print(f"    scripts: {skill.scripts}")

# ======================== 创建带技能的Agent ========================
agent = Agent(
    model=myModel,
    skills=skills,  # 加载技能后，Agent自动获得3个tool:get_skill_instructions,get_skill_refrences,get_skill_script
    instructions=["按照技能指南进行代码审查", "简洁输出"],
    debug_mode=True,
)

# Agent会自动调用 get_skill_instructions 来获取审查规则
# 然后按照规则审查代码
test_code = """
def getData(X):
    try:
        result = X + 1
        return result
    except:
        pass

class my_class:
    def __init__(self, Items=[]):
        self.items = Items
"""

print("\n" + "=" * 60)
print("请Agent按照code_review技能审查以下代码：")
print("=" * 60)
agent.print_response(f"请用code-review技能审查这段代码：\n```python\n{test_code}\n```")
