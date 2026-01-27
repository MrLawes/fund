# pip install tavily-python-0.7.19

from tavily import TavilyClient

# 联网搜索
tavily_client = TavilyClient(api_key="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")
response = tavily_client.search("Who is Leo Messi?")

print(response)
