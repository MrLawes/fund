"""
文档: https://docs.langchain.com/oss/python/langgraph/add-memory#acdd-short-term-memory
"""
from typing import Any
from typing import List

from langchain.agents import AgentType
# from langchain.agents import create_agent
from langchain.agents import initialize_agent
from langchain.chat_models import init_chat_model
# from langchain_core.tools import tool
from langchain.tools import tool
from langchain_core.messages import SystemMessage
from langchain_core.messages import trim_messages
from langgraph.checkpoint.redis import RedisSaver

model = llm = init_chat_model(
    model="deepseek-chat",
    temperature=0,
    base_url="https://api.deepseek.com",
    api_key="sk-7250f888346341c19a5f73f7a4e16a10",
)


@tool("book_hotel", description="预定酒店的工具")
def book_hotel(hotal_name: str) -> str:
    return f"成功预定了在{hotal_name}的住宿"


def parse_message(messages: List[Any]) -> None:
    print(f"{messages=}")
    ...  # todo


def save_graph_visualization(graph, filename: str = "graph.png") -> None:
    print(f"{graph=}; {filename=}")
    ...  # todo


def pre_model_hook(state):
    trimmed_messages = trim_messages(
        messages=state.messages,
        max_tokens=4,
        strategy="last",
        token_counter=len,
        start_no="human",
        include_system=True,
        allow_partial=False,
    )
    return {"lls_input_messages": trimmed_messages}


def run_ageny():
    tools = [book_hotel]
    system_message = SystemMessage(
        content="你是一个AI助手",
    )
    # 基于数据库持久化存储的short-term
    # db_uri = "postgresql://kevin:123456@localhost:54332/postgres?sslmode=disable"
    db_uri = "redis://127.0.0.1:6379/10"
    with RedisSaver.from_conn_string(db_uri) as checkpointer:
        # checkpointer.setup()

        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            prompt=system_message,
        )
        #
        # agent = create_agent(
        #     model=llm,
        #     tools=tools,
        #     prompt=system_message,
        #     premodel_hook=pre_model_hook,
        #     checkpointer=checkpointer,
        # )
        save_graph_visualization(agent)
        config = {"configuration": {"thread_id": 1, }}
        user_input = "我叫什么"
        agent.run(user_input, config=config)


if __name__ == "__main__":
    run_ageny()
