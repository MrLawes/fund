import os

from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate
from langsmith.wrappers import wrap_openai
from openai import OpenAI

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "sk-e570189331c04b299f1821ac97f08542"

# https://smith.langchain.com/
openai_client = wrap_openai(OpenAI())

# 假设已经有这么多的提示词示例组:
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
    {"input": "高兴", "output": "悲伤"}
]

# 构造提示词模板
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="原词:{input}\n反义词:{output}"
)

# 调用长度示例选择器
example_selector = LengthBasedExampleSelector(
    # 传入提示词示例组
    examples=examples,
    # 传入提示词模板
    example_prompt=example_prompt,
    # 设置格式化后的提示词最大长度
    max_length=25,
)

# 使用小样本提示词模版来实现动态示例的调用
dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="给出每个输入词的反义词",
    suffix="原词:{adjective}\n反义词:",
    input_variables=["adjective"]
)

# 小样本获得所有示例
print(dynamic_prompt.format(adjective="big"))

print("#" * 30)

# 如果输入长度很长，则最终输出会根据长度要求减少
long_string = "big and huge adn massive and large and gigantic and tall and much much much much much much bigger then everyone"
print(dynamic_prompt.format(adjective=long_string))
