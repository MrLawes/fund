"""
文档: https://docs.langchain.com/oss/python/langgraph/add-memory#acdd-short-term-memory
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
"""

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import trim_messages
from langchain_core.tools import tool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent  # noqa
from langgraph.store.postgres import PostgresStore

llm = init_chat_model(
    model="deepseek-chat",
    temperature=0,
    base_url="https://api.deepseek.com/v1",
    api_key="sk-7250f888346341c19a5f73f7a4e16a10",
)


@tool("book_hotel", description="预定酒店的工具")
def book_hotel(hotal_name: str) -> str:
    return f"成功预定了在{hotal_name}的住宿"


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


def run_ageny():
    tools = [book_hotel]
    system_message = SystemMessage(
        content="你是一个AI助手",
    )

    # 基下做摆库持久化存储的short-term
    db_uri = "postgresql://postgres:admin@localhost:5432/postgres?sslmode=disable"
    # mac: brew install postgresql
    with PostgresSaver.from_conn_string(db_uri) as checkpointer:
        with PostgresStore.from_conn_string(db_uri) as store:
            checkpointer.setup()
            store.setup()

            agent = create_react_agent(  # noqa
                model=llm,  # noqa
                tools=tools,
                prompt=system_message,
                pre_model_hook=pre_model_hook,
                checkpointer=checkpointer,  # 短期记忆
                store=store,  # 长期记忆
            )

            config = {"configurable": {"thread_id": 1, "user_id": "陈海鸥"}}
            user_id = config["configurable"]["user_id"]
            namespace = ("memories", user_id)

            memory1 = "我的名字叫kevin"
            store.put(namespace, "36b0976bcc4f4f40abdd6a09d99394ef", {"data": memory1})
            memory2 = "我的住宿偏好是: 有窗户,有 Wi-Fi"
            store.put(namespace, "1ad7c846c4d84848bb9f79567f3a8512", {"data": memory2})

            memories = store.search(namespace, query="")
            info = " ".join([d.value["data"] for d in memories]) if memories else "无长期记忆信息"
            user_input = f"预定一个汉庭酒店,我的附加信息有:{info}"
            print(f"{user_input=}")

            # user_input = "我叫什么"
            # user_input="我是kevin"
            # user_input="我叫什么"
            # user_input="预定一个汉庭酒店"
            # user_input = f"我叫什么"
            agent_response = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=config
            )
            agent_response_content = agent_response["messages"][-1].content
            print(f"{agent_response_content=}")


if __name__ == "__main__":
    run_ageny()
