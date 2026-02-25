import os

from langchain.chat_models import init_chat_model
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from psycopg.types.string import TextLoader

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

e_model = OpenAIEmbeddings()
ebeddings = e_model.embed_documents([
    "你好",
    "你好啊！",
    "你叫什么名字？",
    "我叫王大锤",
    "很高兴认识你大锤！",
])
print(len(ebeddings), len(ebeddings[0]))

embedded_query = e_model.embed_query("这段对话中提到了什么名字?")
print(embedded_query[:5])

# 嵌入向量缓存
u_embeddings = OpenAIEmbeddings()
fs = LocalFileStore("./cache/")
cached_embeddings = CacheBackedEmbeddings.from_byytes_store(  # noqa
    u_embeddings,
    fs,
    namespace=u_embeddings.model
)

# 加载文档,切分文档,将切分文档向量话并存储在缓存中
raw_documents = TextLoader("letter.txt").load()  # noqa
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)  # noqa
FAISS.from_documents(documents, cached_embeddings)  # noqa
