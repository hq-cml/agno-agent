# demo03_2: 使用工具进阶---工具集
from agno.agent import Agent
from agno.tools import tool
from agno.tools import Toolkit

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from demo.create_model import create_model

# 准备一个模型
myModel = create_model()

# 自定义工具
@tool
def getWeather(city: str) -> str:
    """
    获取city对应的天气

    Args:
        city: 城市名称，如"北京“

    Returns:
        天气描述字符串
    """
    return f"{city}今天晴朗，气温25度"

# Toolkit，相当于是同一类工具的集合，实现上通常是一个类
class FileToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="file_tools", tools=[
            self.read_file,
            self.write_file,
            self.append_file,
            self.list_dir,
            self.file_exists,
            self.delete_file,
        ])

    def read_file(self, path: str) -> str:
        """读取文件内容

        Args:
            path: 文件路径

        Returns:
            文件内容字符串
        """
        with open(path, 'r') as f:
            return f.read()

    def write_file(self, path: str, content: str) -> str:
        """写入文件内容（覆盖写入，文件不存在则创建）

        Args:
            path: 文件路径
            content: 要写入的内容

        Returns:
            写入成功的提示信息
        """
        with open(path, 'w') as f:
            f.write(content)
        return f"已写入{path}"

    def append_file(self, path: str, content: str) -> str:
        """追加内容到文件末尾

        Args:
            path: 文件路径
            content: 要追加的内容

        Returns:
            追加成功的提示信息
        """
        with open(path, 'a') as f:
            f.write(content)
        return f"已追加内容到{path}"

    def list_dir(self, path: str = ".") -> str:
        """列出目录下的文件和子目录

        Args:
            path: 目录路径，默认为当前目录

        Returns:
            目录内容列表，每行一个条目，目录以/结尾
        """
        entries = os.listdir(path)
        result = []
        for entry in sorted(entries):
            full = os.path.join(path, entry)
            if os.path.isdir(full):
                result.append(f"{entry}/")
            else:
                result.append(entry)
        return "\n".join(result)

    def file_exists(self, path: str) -> str:
        """检查文件或目录是否存在

        Args:
            path: 文件或目录路径

        Returns:
            存在返回"存在"，否则返回"不存在"
        """
        if os.path.exists(path):
            file_type = "目录" if os.path.isdir(path) else "文件"
            return f"{path} 存在，类型为{file_type}"
        return f"{path} 不存在"

    def delete_file(self, path: str) -> str:
        """删除文件

        Args:
            path: 要删除的文件路径

        Returns:
            删除结果提示信息
        """
        if not os.path.exists(path):
            return f"{path} 不存在，无需删除"
        if os.path.isdir(path):
            return f"{path} 是目录，不能用此工具删除"
        os.remove(path)
        return f"已删除{path}"

agent = Agent(
    name="agno v0.1",
    model=myModel,
    tools=[
        getWeather,    # 使用自定义工具
        FileToolkit(), # 使用工具集
    ],
    description="你是一个通用Agent，负责回答各类问题或者执行一些力所能及的任务。",
    instructions="如果有符合条件的tool，优先使用tool！",
    debug_mode=True,
)

#ret = agent.run("北京天气如何？")
#ret = agent.run("当前目录创建一个文件test.txt，并写入hello world")
#ret = agent.run("看一下当前目录是否存在test.txt，如果存在则追加写入一行hello agno。如果不存在则创建一个test.txt文件。")
ret = agent.run("看一下当前目录都有哪些文件？")

print(f"\n\n\n-----------------------------\n运行结果如下：\n{ret.content}")

