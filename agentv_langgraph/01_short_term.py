"""
文档: https://docs.langchain.com/oss/python/langgraph/add-memory#acdd-short-term-memory
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
"""

import asyncio
import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import trim_messages
from langchain_core.tools import tool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.prebuilt import create_react_agent
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from tavily import TavilyClient

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "sk-7250f888346341c19a5f73f7a4e16a10"

# LangSmith : 它能让您密切监控和评估您的应用程序，从而帮助您快速、自信地交付产品。
openai_client = wrap_openai(OpenAI())

llm = init_chat_model(
    model="deepseek-chat",
    temperature=0,
    base_url="https://api.deepseek.com/v1",
    api_key="sk-7250f888346341c19a5f73f7a4e16a10",
)


@tool("book_hotel", description="预定酒店的工具")
def book_hotel(hotal_name: str) -> str:
    return f"成功预定了在{hotal_name}的住宿"


@tool("tavily", description="联网搜索的工具")
def tavily(query: str) -> str:
    """
    联网搜索工具，接收用户查询内容并返回搜索结果。

    Args:
        query (str): 用户输入的搜索关键词。

    Returns:
        str: 搜索结果的摘要信息。
    """
    # 初始化 TavilyClient 实例
    tavily_client = TavilyClient(api_key="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")

    try:
        # 调用搜索接口
        response = tavily_client.search(query)

        # 提取搜索结果中的关键信息
        results = response.get("results", [])
        if not results:
            return "未找到相关搜索结果。"

        # 构造返回内容（示例：取前3条结果）
        formatted_results = "\n".join(
            [f"{i + 1}. {item['title']}: {item['content'][:100]}..." for i, item in enumerate(results[:3])]
        )
        return f"搜索结果：\n{formatted_results}"

    except:  # noqa
        return "搜索失败"


def pre_model_hook(state):
    trimmed_messages = trim_messages(
        messages=state["messages"],
        max_tokens=4,
        strategy="last",
        token_counter=len,
        start_on="human",
        include_system=True,
        allow_partial=False,
    )
    return {"lls_input_messages": trimmed_messages}


async def run_ageny():
    tools = [book_hotel, tavily]
    system_message = SystemMessage(
        content="你是一个AI助手",
    )

    # 基下做摆库持久化存储的short-term
    db_uri = "postgresql://postgres:admin@localhost:5432/postgres?sslmode=disable"
    # mac: brew install postgresql
    async with AsyncPostgresSaver.from_conn_string(db_uri) as checkpointer:
        await checkpointer.setup()

        agent = create_react_agent(  # noqa
            model=llm,  # noqa
            tools=tools,
            prompt=system_message,
            pre_model_hook=pre_model_hook,
            checkpointer=checkpointer,
        )
        config = {"configurable": {"thread_id": "2026-02-11", }}
        # user_input = "我叫什么"
        # user_input="我叫海鸥"
        user_input = "我叫什么"
        # user_input="预定一个汉庭酒店"
        # user_input = f"我叫什么"
        # user_input = "最近今晨怎么了"
        agent_response = await agent.ainvoke({"messages": [HumanMessage(content=user_input)]}, config=config)  # noqa
        agent_response_content = agent_response["messages"][-1].content
        print(f"{agent_response_content=}")


if __name__ == "__main__":
    asyncio.run(run_ageny())
