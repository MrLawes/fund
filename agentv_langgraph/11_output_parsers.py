import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

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


# 定义个数据模型,用来描述最终的实例结构
class Joke(BaseModel):
    setup: str = Field(description="设置笑话的问题")
    punchline: str = Field(description="回答笑话的答案")

    @classmethod
    @field_validator("setup")
    def question_mark(cls, field):
        if field[-1] != "?":
            raise ValueError("不符合预期的问题格式")
        return field


# 将Joke数据模型传入
parser = PydanticOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="回答用户的输入.\n{{format_instructions}}\n{{query}}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

parser2 = CommaSeparatedListOutputParser()

prompt2 = PromptTemplate(
    template="列出5个{subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": parser2.get_format_instructions()}
).format(subject="常见的中国人名字")

if __name__ == "__main__":
    agent = create_react_agent(  # noqa
        model=llm,  # noqa
        tools=[],
        prompt=prompt,
    )
    config = {"configurable": {"thread_id": "2026-02-12", }}
    # agent_response = agent.invoke({"query": [HumanMessage(content="给我讲一个笑话")]}, config=config)  # noqa
    # agent_response_content = agent_response["messages"][-1].content
    # print(parser.parse(agent_response_content))

    agent = create_react_agent(  # noqa
        model=llm,  # noqa
        tools=[],
        prompt=prompt2,
    )
    agent_response = agent.invoke({"messages": [HumanMessage(content="")]}, config=config)  # noqa
    agent_response_content = agent_response["messages"][-1].content
    print(parser2.parse(agent_response_content))
