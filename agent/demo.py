"""
pip uninstall langchain langchain-core langchain-community langchain-openai
pip install langchain==0.2.15
pip install langchain-core==0.2.36
pip install langchain-community==0.2.15
pip install langchain-openai==0.1.24
"""

import os

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


def get_wikipedia(query):  # noqa
    return f"北京是中华人民共和国的首都，位于华北平原北部，是中国的政治、文化、国际交往和科技创新中心。  "  # 返回字符串而不是字典


agent = initialize_agent(
    [
        Tool(
            name="Weather",
            func=get_weather,
            description="查询城市天气",
        ),
        Tool(
            name="Wikipedia",
            func=get_wikipedia,
            description="查询百科的介绍",
        ),
    ],
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # 反应式推送
    verbose=True,
    handle_parsing_errors=True
)

print(agent.invoke({"input": "给我一些北京信息"}))
print(agent.invoke({"input": "今天北京天气如何"}))
