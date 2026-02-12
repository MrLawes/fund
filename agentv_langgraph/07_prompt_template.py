import inspect
import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.prompts import StringPromptTemplate
from langgraph.prebuilt import create_react_agent
from langsmith.wrappers import wrap_openai
from openai import OpenAI

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "sk-e570189331c04b299f1821ac97f08542"

# https://smith.langchain.com/
openai_client = wrap_openai(OpenAI())


def hello_world():
    print("hello world")


PROMPT = """你是一个非常有经验和天赋的程序员,现在给你如下函数名称,你会按照如下格式,输出这段代码的名称、源代码、中文解释。
函数名称:{function_name}
源代码:
{source_code}
代码解释:
"""


def get_source_code(function_name):
    return inspect.getsource(function_name)


class CustmPrompt(StringPromptTemplate):
    def format(self, **kwargs) -> str:
        # 获得源代码
        source_code = get_source_code(kwargs["function_name"])
        # 生成提示词模板
        prompt = PROMPT.format(
            function_name=kwargs["function_name"].__name__, source_code=source_code,
        )
        return prompt


a = CustmPrompt(input_variables=["function_name"])
pm = a.format(function_name=hello_world)

# 创建一个LLM
llm = init_chat_model(
    model="deepseek-chat",
    temperature=0,  # 灵敏度
    base_url="https://api.deepseek.com/v1",
    api_key="sk-e570189331c04b299f1821ac97f08542",
)

agent = create_react_agent(  # noqa
    model=llm,  # noqa
    tools=[],
    prompt=pm,
)
#
if __name__ == "__main__":
    agent_response = agent.invoke({"messages": [HumanMessage(content="")]})
    agent_response_content = agent_response["messages"][-1].content
    print(f"{agent_response_content}")
