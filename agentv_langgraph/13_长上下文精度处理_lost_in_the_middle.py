import os

from langchain.chat_models import init_chat_model
from langchain_classic.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_classic.chains.llm import LLMChain
from langchain_community.document_transformers import LongContextReorder
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
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

# 使用huggingface托管的开源LLM来做嵌入,MiniLM-L6-v2是一个较小的LLM
embedings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")

text = [
    "篮球是一项伟大的运动。",
    "带我飞往月球是我最喜欢的歌曲之一。",
    "凯尔特人队是我最喜欢的球队。",
    "这是一篇关于波士顿凯尔特人的文件。",
    "我非常喜欢去看电影。",
    "波士顿凯尔特人队以20分的优势赢得了比赛。",
    "这只是一段随机的文字。",
    "《艾尔登之环》是过去15年最好的游戏之一。",
    "L.科内特是凯尔特人队最好的球员之一。",
    "拉里.伯德是一位标志性的NBA球员。",
]
retrieval = Chroma.from_texts(text, embedings).as_retriever(
    search_kwargs={"k": 10}
)

query = "关于凯尔特人队你知道什么？"

# 根据相关性返回文本块
docs = retrieval._get_relevant_documents(query, run_manager=None)  # noqa
print(f"{docs=}")

# 对检索结果进行重新排序,根据论文的方案
# 问题相关性越低的内容块放在中间
# 问题相关性越高的内容块放在头尾
reordering = LongContextReorder()
reo_docs = reordering.transform_documents(docs)
print(f"{reo_docs=}")

document_prompt = PromptTemplate(
    input_variables=["page_content"],
    template="{page_content}",
)

stuff_prompt_override = """ Given this text extractts:
-----------------------------------------
{context}
-----------------------------------------
Please answer the following questions:
{query}
"""

prompt = PromptTemplate(
    input_variables=["context", "query"],
    template=stuff_prompt_override,
)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt
)

WorkChain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_prompt=document_prompt,
    document_variable_name="context"
)

# 调用
result = WorkChain.run(
    input_documents=reo_docs,
    query="凯尔特人队是哪里的球队?"
)

# 总结: 各种文档->各种 Loader -> 文本切片 -> 嵌入向量化 -> 向量存储 -> 各种检索链
print(f"{result=}")
