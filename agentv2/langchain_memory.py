import os  # noqa

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 设置 API 密钥
os.environ["OPENAI_API_KEY"] = "sk-7250f888346341c19a5f73f7a4e16a10"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"


def get_weather(location):
    # 修复逻辑：根据传入的位置返回相应的天气
    if "北京" in location or "beijing" in location.lower():
        return f"{location}的天气是晴天"
    elif "上海" in location or "shanghai" in location.lower():
        return f"{location}的天气是大暴雨"  # 修改为正确的天气
    else:
        return f"{location}的天气是多云"


def get_wikipedia(query):  # noqa
    return f"北京是中华人民共和国的首都，位于华北平原北部，是中国的政治、文化、国际交往和科技创新中心。"


# 定义一个简单Prompt模板
prompt = ChatPromptTemplate.from_template("""
你是一位贴心的AI助手,现在和用户聊天。
请根据对话历史和最新提问,给出自然、有帮助的回答。
对话历史:
{history}
用户提问:
{input}
请回答:
""")

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
    model="deepseek-chat",  # 文本生成模型
    # model="deepseek-reson",  # 推理模型
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=10,
)

# 初始化带记忆功能的代理
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    # verbose=True,
    memory=memory,
    prompt=prompt,
)

# 使用示例
# print(agent_chain.run("北京的天气如何"))
# print(agent_chain.run("上海的呢"))

print(agent_chain.run("今天北京的天气如何?"))
print(agent_chain.run("今天去旅游适合穿什么衣服?"))
print(agent_chain.run("请告诉我：去这个地方有哪些景点推荐？"))
