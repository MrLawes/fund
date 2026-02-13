import os

from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langsmith.wrappers import wrap_openai
from openai import OpenAI

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "sk-e570189331c04b299f1821ac97f08542"

# https://smith.langchain.com/
openai_client = wrap_openai(OpenAI())

# 输出函数参数
llm = init_chat_model(
    model="deepseek-chat",
    temperature=0,
    base_url="https://api.deepseek.com/v1",
    api_key="sk-e570189331c04b299f1821ac97f08542",
)

# 数据加载
loader = TextLoader("12_loader.md")
print(loader.load())

loader = CSVLoader("12_loader.csv")
print(loader.load())

loader = CSVLoader("12_loader.csv", source_column="Project")
print(loader.load())

loader = JSONLoader("09_load_prompt.json", jq_schema=".template", text_content=False)
print(loader.load())

loader = PyPDFLoader("12_loader.pdf")
print(loader.load_and_split())

# if __name__ == "__main__":
#     agent = create_react_agent(  # noqa
#         model=llm,  # noqa
#         tools=[],
#     )
#     config = {"configurable": {"thread_id": "2026-02-12", }}
#
#     agent_response = agent.invoke({"messages": [HumanMessage(content="")]}, config=config)  # noqa
#     agent_response_content = agent_response["messages"][-1].content
#     print(f"{agent_response_content=}")
