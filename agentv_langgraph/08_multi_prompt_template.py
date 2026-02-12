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

# Final Prompt由一系列变量构成
full_template = """{Character}
{behavior}
{prohibit}
"""

full_prompt = PromptTemplate.from_template(full_template)

# 第一层基本性格设计
Character_template = """你是{person},你有着{xingge}."""
character_prompt = PromptTemplate.from_template(Character_template)

# 第二层行为设计
behavior_template = """你遵从以下的行为:
{behavior_list}
"""
behavior_prompt = PromptTemplate.from_template(behavior_template)

# 第三层不允许的行为
prohibit_template = """你不允许有以下行为:
{prohibit_list}
"""
prohibit_prompt = PromptTemplate.from_template(prohibit_template)

input_prompts = [
    ("Character", character_prompt),
    ("behavior", behavior_prompt),
    ("prohibit", prohibit_prompt)
]

pipeline_prompt = PipelinePromptTemplate(final_prompt=full_prompt, pipeline_prompts=input_prompts)  # noqa

pipeline_prompt.format(
    person="埃隆马斯克",
    xingge="钢铁般的意志,你是世界首富,精通物理、天文、商业,你是商业奇才,你的终极梦想是殖民火星。",
    behavior_list="1.你喜欢冒险\n2.你非常崇拜爱因斯坦\n3.你总是乐于助人,回答用户各种问题.",
    prohibit_list="1.你不可以说自己是一个人工智能助手或者音机器人\n2.当你不知道答案的时候,可以说让我再想想。"
)

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
    prompt=pipeline_prompt,
)

if __name__ == "__main__":
    agent_response = agent.invoke({"messages": [HumanMessage(content="")]})  # noqa
    agent_response_content = agent_response["messages"][-1].content
    print(f"{agent_response_content}")
