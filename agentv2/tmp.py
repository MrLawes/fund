import os

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import Field

# 设置 API 密钥
os.environ["OPENAI_API_KEY"] = "sk-7250f888346341c19a5f73f7a4e16a10"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,  # 最稳定
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


#
# class HeWeatherTool(BaseTool):
#     name: str = Field(default="heweather_tool", description="工具名称")
#     description: str = Field(default="用来查询指定城市的实时天气,支持中文城市名", )
#
#     def _run(self, query: str, run_manager=None) -> str:
#         print(f"{query=}")
#         result = "当前天气: 暴雨,温度 23°C"
#         memory.save_context({"input": query}, {"output": result})
#         return result

class HeWeatherTool(BaseTool):
    name: str = Field(default="heweather_tool", description="查询指定城市实时天气的工具")
    description: str = Field(
        default="用来查询指定城市的实时天气,支持中文城市名。当被问及与天气相关的问题时，请使用此工具获取准确的天气信息。", )

    def _run(self, query: str, run_manager=None) -> str:
        print(f"{query=}")
        result = "北京当前天气: 暴雨, 温度: 23°C"
        memory.save_context({"input": query}, {"output": result})
        # memory.save_context({"input": query}, {"output": f"Action Input: {query} {result}"})
        return result


tools = [HeWeatherTool()]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # 反应式推送
    memory=memory,
    verbose=True,
    # handle_parsing_errors=True,  # 添加这一行
)

weahter_response = agent.run("今天北京的天气如何?")
# print("查询后的内存内容:", memory.load_memory_variables({}))
print("天气查询结果:", weahter_response)

memory_history = memory.load_memory_variables({})
# print("查询后的内存内容:", memory_history)

history_response = agent.run("今天去旅游适合穿什么衣服?")
print("穿衣查询结果:", weahter_response)
# print("查询后的内存内容:", memory.load_memory_variables({}))

# chat_history = memory.load_memory_variables({})["chat_history"]
# print("当前对话历史:", chat_history)

question = "请告诉我：去这个地方有哪些景点推荐？"
# question = f"根据之前你提到的地点和天气：\n{chat_history}\n请告诉我：去这个地方有哪些景点推荐？"
response = agent.run(question)  # 调用f代理
print("景点推荐：", response)

#
#
# ##################################################
#
#
# def get_weather(location):
#     # 修复逻辑：根据传入的位置返回相应的天气
#     if "北京" in location or "beijing" in location.lower():
#         return f"{location}的天气是晴天"
#     elif "上海" in location or "shanghai" in location.lower():
#         return f"{location}的天气是大暴雨"  # 修改为正确的天气
#     else:
#         return f"{location}的天气是多云"
#
#
# def get_wikipedia(query):  # noqa
#     return f"北京是中华人民共和国的首都，位于华北平原北部，是中国的政治、文化、国际交往和科技创新中心。"
#
#
# # 定义一个简单Prompt模板
# prompt = ChatPromptTemplate.from_template("""
# 你是一位贴心的AI助手,现在和用户聊天。
# 请根据对话历史和最新提问,给出自然、有帮助的回答。
# 对话历史:
# {history}
# 用户提问:
# {input}
# 请回答:
# """)
#
# # 创建工具列表
# tools = [
#     Tool(
#         name="天气查询",
#         func=get_weather,
#         description="用于查询指定地点的天气情况"
#     ),
#     Tool(
#         name="维基百科",
#         func=get_wikipedia,
#         description="用于获取百科知识"
#     )
# ]
#
# # 初始化带记忆功能的代理
# agent_chain = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
#     # verbose=True,
#     memory=memory,
#     prompt=prompt,
# )
#
# # 使用示例
# print(agent_chain.run("北京的天气如何"))
# print(agent_chain.run("上海的呢"))
