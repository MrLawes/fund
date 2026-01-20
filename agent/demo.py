"""
pip uninstall langchain langchain-core langchain-community langchain-openai
pip install langchain==0.2.15
pip install langchain-core==0.2.36
pip install langchain-community==0.2.15
pip install langchain-openai==0.1.24
"""

import os

import wikipedia
from langchain.agents import AgentType
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI

# 设置 API 密钥
os.environ["OPENAI_API_KEY"] = "sk-7250f888346341c19a5f73f7a4e16a10"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

# 创建 DeepSeek 模型实例
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def get_weather(location):
    return f"{location}的天气是大暴雨"  # 返回字符串而不是字典


agent = initialize_agent(
    [
        Tool(
            name="Weather",
            func=get_weather,
            description="Useful for when you need to get the weather in a specific location",
        ),
        Tool(
            name="Wikipedia",
            func=lambda query: wikipedia.summary(query, sentences=2),
            description="Useful for when you need to get information from Wikipedia",
        ),
    ],
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # 注意参数名变更
    verbose=True,
)

result = agent.invoke({"input": "今天北京天气如何"})
print(result)
