import os

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

# 设置 API 密钥
os.environ["OPENAI_API_KEY"] = "sk-7250f888346341c19a5f73f7a4e16a10"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"


def get_weather(location):
    return f"{location}的天气是大暴雨"


def get_wikipedia(query):
    return f"北京是中华人民共和国的首都，位于华北平原北部，是中国的政治、文化、国际交往和科技创新中心。"


# 创建工具列表
tools = [
    Tool(
        name="天气查询",
        func=get_weather,
        description="用于查询指定地点的天气情况"
    ),
    Tool(
        name="维基百科",
        func=get_wikipedia,
        description="用于获取百科知识"
    )
]

# 创建模型实例
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 初始化带记忆功能的代理
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # 支持对话记忆
    # verbose=True,
    memory=memory
)

# 使用示例
print(agent_chain.run("你好,你是谁?"))
print(agent_chain.run("你能帮我写一个PythonHelloWorld程序吗?"))
print(agent_chain.run("再帮我写一个Java版本的吧!"))
