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
# 优秀的提示词:
# 【立角色】:引导AI进入具体场景,赋予其行家身份:     假如你是导游
# 【述问题】:告诉AI你的困惑和问题,以及背景信息:     找要到海南游玩,预算一万元,旅行人数三个人,行程7天
# 【定目标】:告诉AI你的需求,希望达成的目标:        请帮我做一份旅行攻略
# 【补要求】:告诉AI回答时注意什么,或者如何回复:     请注意:我不喜欢行程太紧凑,我不喜欢网红景点,更喜欢有文化底蕴的聚点. 另外,推荐最点请附上各个的量点价格。

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
