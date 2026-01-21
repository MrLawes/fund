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
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def get_weather(location):
    return f"{location}的天气是大暴雨"  # 返回字符串而不是字典


def get_wikipedia(query):  # noqa
    return f"北京是中华人民共和国的首都，位于华北平原北部，是中国的政治、文化、国际交往和科技创新中心。  "  # 返回字符串而不是字典


agent = initialize_agent(
    tools=[
        Tool(
            name="Weather",
            func=get_weather,
            description="查询城市天气(中文),例如:'上海'、'北京'、'长沙'",
        ),
        Tool(
            name="Wikipedia",
            func=get_wikipedia,
            description="查询百科的介绍",
        ),
    ],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # 反应式推送
    verbose=True,
    handle_parsing_errors=True
)

# print(agent.invoke({"input": "给我一些北京信息"}))
print(agent.invoke({"input": "今天北京天气如何"}))
# 和大语音模型交互:
# 1. Answer the following questions as best you can. You have access to the following tools:
# Weather(location) - 查询城市天气(中文),例如:'上海'、'北京'、'长沙'
# Wikipedia(query) - 查询百科的介绍
# Use the following format:
# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [Weather, Wikipedia]
# Action Input: the input to the action
# Observation: the result of the action
# (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: 今天北京天气如何\nThought:"

# 2. Answer the following questions as best you can. You have access to the following tools:
# Weather(location) - 查询城市天气(中文),例如:'上海'、'北京'、'长沙'
# Wikipedia(query) - 查询百科的介绍
# Use the following format:
# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [Weather, Wikipedia]
# Action Input: the input to the action
# Observation: the result of the action
# (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: 今天北京天气如何
# Thought:Thought: 用户询问北京今天的天气，我需要使用天气查询工具。
# Action: Weather  Action Input: 北京  Observation: 北京  \n的天气是大暴雨\nThought:
