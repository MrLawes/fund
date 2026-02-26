import os

from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
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
        self.documents = []

    def get_docx_file(self):
        loader = Docx2txtLoader("15_房屋租赁合同.docx")  # noqa
        text = loader.load()
        self.documents.append(text)
        return text

    def get_pdf_file(self):
        loader = PyPDFLoader("12_loader.pdf")  # noqa
        text = loader.load()
        self.documents.append(text)
        return text

    def get_xlsx_file(self):
        loader = UnstructuredExcelLoader("12_loader.xlsx")  # noqa
        text = loader.load()
        self.documents.append(text)
        return text

    def split_sentences(self):
        """ 处理文档的函数 """
        for document in self.documents:
            print(f"{document=}")
            if document is not None:
                text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
                print(f"{text_splitter.split_documents(document)=}")


chat_doc = ChatDoc()
result = chat_doc.get_docx_file()
print(f"{result=}")

result = chat_doc.get_pdf_file()
print(f"{result=}")

result = chat_doc.get_xlsx_file()
print(f"{result=}")

# 处理文档的函数
chat_doc.split_sentences()
