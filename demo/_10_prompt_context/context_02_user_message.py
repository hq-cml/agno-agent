# demo10_02: User Message - 每次请求的动态信息
# 展示 dependencies 注入和 add_dependencies_to_context 的效果

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

from agno.agent import Agent

myModel = create_model()

# ======================== dependencies注入 ========================
# dependencies会以JSON格式追加到user message中，Agent可以引用这些信息
agent = Agent(
    name="课程助手",
    model=myModel,
    description="你是一个编程课程助手",
    instructions=[
        "根据用户的级别调整回答深度",               # 这个很重要，否则LLM不知道dependencies是啥意思
        "参考dependencies中的用户信息来个性化回答",
    ],
    add_dependencies_to_context=True,          # 必须开启，否则dependencies不会注入到消息中
    debug_mode=True,
)

# run时通过dependencies传入动态上下文
# 这些信息会注入到user message中，不同用户可以传不同的值，如下是通过Debug查看的user message信息：

#  解释一下什么是闭包
#
#       <additional context>
#       {
#         "user_level": "\u521d\u7ea7",
#         "language": "Python",
#         "learning_goal":
#       "\u7406\u89e3\u51fd\u6570\u5f0f\u7f16\u7a0b\u57fa\u7840"
#       }
#       </additional context>   :
ret = agent.run(
    "解释一下什么是闭包",
    dependencies={
        "user_level": "初级",
        "language": "Python",
        "learning_goal": "理解函数式编程基础",
    },
    debug_mode=True,
)
print(f"\n回复：{ret.content}\n")
