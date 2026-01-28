# 我要从深圳市南山区中兴大厦驾车到宝安区宝安体育馆,帮我规划下路径
# 深圳的天气如何

"""
pip uninstall langgraph langchain langchain-deepseek langchain-openai langchain-mcp-adapters -y
pip install langgraph==0.0.60
pip install langchain==1.2.6
pip install langchain-deepseek==1.0.1
pip install langchain-openai==1.1.7
pip install langchain-mcp-adapters==0.1.13
"""

import asyncio
import os
# from langchain.chat_models import init_chat_model
from typing import Any
from typing import List

from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
# from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
# from langchain_community.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

# agent = create_agent("openai:gpt-5", tools=tools)

# from langchain.chat_models import init_chat_model

# MCP 广场: https://modelscope.cn/mcp
# 获取高德地图APIKey
# AMAP_MAPS_API_KEY = os.getenv("AMAP_MAPS_API_KEY")
AMAP_MAPS_API_KEY = "edfc412cca06d24d8xxxx9a1da50887fb44a"

# 设置 API 密钥
os.environ["OPENAI_API_KEY"] = "sk-7250f888346341c19a5f73f7a4e16a10"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

# 使用 langgraph推荐方式定义大模型
# 也可以使用本地私有化部署模型(数据安全)
# llm = init_chat_model(
#     model="deepseek-chat",
#     # model="deepseek-reasoner",
#     temperature=0,
#     model_provider="deepseek",
# )

llm = ChatOpenAI(
    model="deepseek-chat",  # 文本生成模型
    # model="deepseek-reasoner",  # 推理模型
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=10,
)


# tavily 联网搜索

# 解析消息列表
def parse_messages(messages: List[Any]) -> None: ...


# 保存状态图的可视化表示
def save_graph_visualization(graph, filename: str = "graph.png") -> None: ...


async def run_agent():
    # 实例化MCP Server客户端
    client = MultiServerMCPClient({
        # 高德地图MCP Server
        "amap-amap-sse": {
            "url": "https://mcp.amap.com/sse?key=" + AMAP_MAPS_API_KEY,
            "transport": "sse",  # 长连接
        },
    })

    # 从MCP Server中获取可提供使用的全部工具
    tools = await client.get_tools()
    print(f"tools:{tools}\n")

    # 基于内存存储的short-term
    checkpointer = InMemorySaver()

    # 定义系统消息,指导如何使用工具
    system_message = SystemMessage(content="你是一个AI助手,使用高德地图工具获取信息。")

    # 创建 ReAct风格的 agent
    # agent = create_agent(
    #     model=llm,
    #     tools=tools,
    #     system_prompt=system_message,
    #     checkpointer=checkpointer,
    # )
    # 创建 ReAct风格的 agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_message,
        checkpointer=checkpointer
    )

    # 将定义的agent的graph进行可视化输出保存至本地
    # save_graph_visualization(agent)
    # 定义short-term需使用的thread_id
    config = {"configurable": {"thread_id": "1"}}

    # 1、非流式处理查询
    # 高德地图接口测试
    agent_response = await agent.ainvoke(
        {"messages": [HumanMessage(content="这个114.05571,22.52245经纬度对应的地方是哪里")]},
        config=config,
    )
    parse_messages(agent_response['messages'])
    agent_response_content = agent_response["messages"][-1].content
    print(f"agent_response:{agent_response_content}")


if __name__ == "__main__":
    asyncio.run(run_agent())
