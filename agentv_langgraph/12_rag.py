import os

from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

# 文档转换器
# 原理
# 1.将文档分成小的、有意义的块(句子)。
# 2.将小的块组合成一个更大的块,直到达到一定的大小。
# 3.一旦达到一定的大小,接着开始创建与下一个块重叠的部分.

with open("12_text.txt") as f:
    zuizhonghuanxiang = f.read()

# 按文档切割: 使用递归字符切分器
text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=50,  # 切分的文本块大小,一般通过长度函数计算
    chunk_overlap=20,  # 切分的文本块重叠大小,一般通过长度函数计算
    length_function=len,  # 长度函数,也可以传递tokenize函数
    add_start_index=True,  # 是否添加开始索引
)
text = text_spliter.create_documents([zuizhonghuanxiang])
print(text[0])
print(text[1])

# 按字符切割

# 使用字符切分器
text_splitter = CharacterTextSplitter(
    separator="。",  # 切割的标识符
    chunk_size=50,  # 切分的文本块大小,一般通过长度函数计算
    chunk_overlap=20,  # 切分的文本块重叠大小,一般通过长度函数计算

)
length_function = len,  # 长度函数,也可以传递tokenize函数
add_start_index = True,  # 是否添加开始索引

# 代码文档的切割
# 要切割的代码文档示例
PYTHON_CODE = """
def hello_world():
    print("hello world")
#调用函数
hello_world()
"""

py_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=50,
    chunk_overlap=20,
)

python_docs = py_splitter.create_documents([PYTHON_CODE])
print(f"{python_docs=}")

# 按token来分割文档
# 加载要切分的文档
with open("12_text.txt") as f:
    zuizhonghuanxiang = f.read()

# 使用字符切分器
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=50,  # 切分的文本块大小,一般通过长度函数计算
    chunk_overlap=20,  # 切分的文本块重叠大小,一般通过长度函数计算
)
text = text_splitter.create_documents([zuizhonghuanxiang])
print(f"{text=}")
