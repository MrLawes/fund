import os

from langchain_core.prompts import load_prompt
from langsmith.wrappers import wrap_openai
from openai import OpenAI

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "sk-e570189331c04b299f1821ac97f08542"

# https://smith.langchain.com/
openai_client = wrap_openai(OpenAI())

prompt = load_prompt("09_load_prompt.yaml")
a = prompt.format(name="小黑", what="恐怖的")

print(a)

prompt = load_prompt("09_load_prompt.json")
b = prompt.format(name="小红", what="搞笑的")

print(b)

prompt = load_prompt("09_prompt_with_output_parser.json")
c = prompt.output_parser.parse("George Washington was born in 1732 and died in 1799.\nScore: 1/2")

print(c)
