import os

# pip install langchain-deepseek==1.0.1
from langchain_deepseek import ChatDeepSeek

os.environ["DEEPSEEK_API_KEY"] = "sk-7250f888346341c19a5f73f7a4e16a10"
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(f"{ai_msg.content=}")
