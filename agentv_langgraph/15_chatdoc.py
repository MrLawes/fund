import os

from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
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


class ChatDoc:

    def __init__(self):
        self.doc = None
        self.splitText = None

    def getFile(self):  # noqa
        doc = self.doc
        loaders = {
            "docx": Docx2txtLoader,
            "pdf": PyPDFLoader,
            "xlsx": UnstructuredExcelLoader,
        }
        file_extension = doc.split(".")[-1]
        loaders_class = loaders.get(file_extension)
        loader = loaders_class(doc)
        text = loader.load()
        return text

    def splitSentences(self):  # noqa
        full_text = self.getFile()
        if full_text != None:  # noqa
            text_splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=20)
            texts = text_splitter.split_documents(full_text)
            self.splitText = texts

    # 向量化与向量存储
    def embeddingAndVectorDB(self):  # noqa
        emmbeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = Chroma.from_documents(documents=self.splitText, embedding=emmbeddings)
        return db

    # 提问并找到相关的文本块
    def askAndFindFiles(self, question):  # noqa
        db = self.embeddingAndVectorDB()
        retriever = db.as_retriever()
        results = retriever.invoke(question)
        return results


chat_doc = ChatDoc()
chat_doc.doc = "15_房屋租赁合同.docx"
chat_doc.splitSentences()
print(f"{chat_doc.splitText=}")
chat_doc.doc = "12_loader.xlsx"
chat_doc.splitSentences()
print(f"{chat_doc.splitText=}")
chat_doc.doc = "12_loader.pdf"
chat_doc.splitSentences()
print(f"{chat_doc.splitText=}")

# 向量化与向量存储
chat_db = chat_doc.embeddingAndVectorDB()
print(f"{chat_db=}")

# 提问并找到相关的文本块
answer = chat_doc.askAndFindFiles("请帮我总结一下")
print(f"{answer=}")
