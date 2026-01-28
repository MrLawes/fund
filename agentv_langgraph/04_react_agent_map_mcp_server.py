# 我要从深圳市南山区中兴大厦驾车到宝安区宝安体育馆,帮我规划下路径
# 深圳的天气如何

"""

pip install langchain==0.1.0+
pip install langchain-core==0.1.0+
pip install langgraph==0.0.60+  # 或更高版本
pip install langchain-mcp-adapters==0.0.1+  # 具体版本根据实际需求


pip uninstall langchain langchain-core langchain-community -y
pip install langchain-core==0.1.47
pip install langchain-community==0.0.33
pip install langchain==0.1.16
pip install langgraph==0.0.63
pip install langchain-mcp-adapters


pip install langgraph==1.0.7
pip install langchain==1.2.6
pip install langchain-deepseek==1.0.1
pip install langchain-openai==1.1.7

"""

import os
# from langchain.chat_models import init_chat_model
from typing import Any
from typing import List

from langchain_core.messages import SystemMessage
# from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

# from langchain.chat_models import init_chat_model

# MCP 广场: https://modelscope.cn/mcp
# 获取高德地图APIKey
# AMAP_MAPS_API_KEY = os.getenv("AMAP_MAPS_API_KEY")
AMAP_MAPS_API_KEY = "edfc412cca06d24d89a1da50887fb44a"

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


def run_agent():
    # 实例化MCP Server客户端
    client = MultiServerMCPClient({
        # 高德地图MCP Server
        "amap-amap-sse": {
            "url": "https://mcp.amap.com/sse?key=" + AMAP_MAPS_API_KEY,
            "transport": "sse",  # 长连接
        },
    })

    # 从MCP Server中获取可提供使用的全部工具
    tools = client.get_tools()
    print(f"tools:{tools}\n")

    # 基于内存存储的short-term
    checkpointer = InMemorySaver()

    # 定义系统消息,指导如何使用工具
    system_message = SystemMessage(content="你是一个AI助手,使用高德地图工具获取信息。")


if __name__ == "__main__":
    run_agent()
    # asyncio.run(run_agent())
