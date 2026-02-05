import asyncio
from typing import Any
from typing import List

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent  # noqa

# MCP 广场: https://modelscope.cn/mcp
# 获取高德地图APIKey: https://console.amap.com/dev/key/app
AMAP_MAPS_API_KEY = "455ae9f6674c851435a309e0fbed217c"

# 使用 langgraph推荐方式定义大模型
# 也可以使用本地私有化部署模型(数据安全)
llm = init_chat_model(
    model="deepseek-chat",
    temperature=0,
    base_url="https://api.deepseek.com/v1",
    api_key="sk-7250f888346341c19a5f73f7a4e16a10",
)


# 解析消息列表
def parse_messages(messages: List[Any]) -> None: ...


# 保存状态图的可视化表示
def save_graph_visualization(graph, filename: str = "graph.png") -> None: ...


# 定义并运行agent
async def run_agent():
    # 实例化MCP Server客户端
    client = MultiServerMCPClient({
        # 高德地图MCPServer
        "amap-amap-sse": {
            "url": "https://mcp.amap.com/sse?key=" + AMAP_MAPS_API_KEY,
            "transport": "sse",
        }
    })

    # 从MCP Server中获取可提供使用的全部工具
    tools = await client.get_tools()
    # print(f"tools:{tools}\n")

    # 基于内存存储的short-term
    checkpointer = InMemorySaver()

    # 定义系统消息,指导如何使用工具
    system_message = SystemMessage(content="你是一个AI助手。")
    # system_message = SystemMessage(content="你是一个AI助手,使用高德地图工具获取信息。")

    # 创建 ReAct风格的 agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_message,
        checkpointer=checkpointer,
    )

    # 将定义的agent的graph进行可视化输出保存至本地
    # save_graph_visualization(agent)
    # 定义short-term需使用的thread_id
    config = {"configurable": {"thread_id": "1"}}

    # 1、非流式处理查询
    # 高德地图接口测试
    agent_response = await agent.ainvoke(
        {"messages": [HumanMessage(content="上海天气如何")]},
        # {"messages": [HumanMessage(content="这个114.05571,22.52245经纬度对应的地方是哪里")]},
        config=config,
    )
    print(f"agent_response:{agent_response=}")
    parse_messages(agent_response['messages'])
    agent_response_content = agent_response["messages"][-1].content
    print(f"agent_response:{agent_response_content}")


if __name__ == "__main__":
    asyncio.run(run_agent())
