import numpy as np  # noqa
from langchain_community.embeddings import DashScopeEmbeddings

from langchain_community.embeddings import HuggingFaceBgeEmbeddings

embedings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")

embeddings = DashScopeEmbeddings(model="text-embedding-v1")
text1 = "运动鞋"
text2 = "手术刀"

vector1 = embeddings.embed_query(text1)
vector2 = embeddings.embed_query(text2)

print(f"{vector1=}")
print(f"{vector2=}")
