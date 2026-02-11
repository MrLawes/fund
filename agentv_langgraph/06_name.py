import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langsmith.wrappers import wrap_openai
from openai import OpenAI

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "sk-e570189331c04b299f1821ac97f08542"

# https://smith.langchain.com/
openai_client = wrap_openai(OpenAI())

# 创建一个LLM
llm = init_chat_model(
    model="deepseek-chat",
    temperature=0,  # 灵敏度
    base_url="https://api.deepseek.com/v1",
    api_key="sk-e570189331c04b299f1821ac97f08542",
)

# 自定义提示词模版
prompt = PromptTemplate.from_template(
    "你是一个起名大师，请模仿示例起3个{county}名字，比如男孩经常被叫做{boy},女孩经常被叫做{girl}.。请返回以逗号分隔的列表形式。仅返回逗号分隔的列表,不要返回其他内容。"
)
message = prompt.format(county="美国男孩", boy="sam", girl="lucy")
agent = create_react_agent(  # noqa
    model=llm,  # noqa
    tools=[],
    prompt=message,
)

if __name__ == "__main__":
    agent_response = agent.invoke({"messages": [HumanMessage(content="帮我取个名字")]})
    agent_response_content = agent_response["messages"][-1].content
    print(f"{agent_response_content=}")
