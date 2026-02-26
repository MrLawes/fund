import os

from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
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

    @staticmethod
    def get_docx_file():
        loader = Docx2txtLoader("15_房屋租赁合同.docx")  # noqa
        text = loader.load()
        return text

    @staticmethod
    def get_pdf_file():
        loader = PyPDFLoader("12_loader.pdf")  # noqa
        text = loader.load()
        return text

    @staticmethod
    def get_xlsx_file():
        loader = UnstructuredExcelLoader("12_loader.xlsx")  # noqa
        text = loader.load()
        return text


result = ChatDoc.get_docx_file()
print(f"{result=}")

result = ChatDoc.get_pdf_file()
print(f"{result=}")

result = ChatDoc.get_xlsx_file()
print(f"{result=}")
