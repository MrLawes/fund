import os

# 文档地址: https://reference.langchain.com/python/integrations/langchain_deepseek/
# pip install langchain-deepseek==1.0.1
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel
from pydantic import Field

os.environ["DEEPSEEK_API_KEY"] = "sk-7250f888346341c19a5f73f7a4e16a10"
model = llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Invoke
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Chinese. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]


# ai_msg = llm.invoke(messages)
# print(f"{ai_msg.content=}")
# print(f"{ai_msg.usage_metadata=}")
# print(f"{ai_msg.response_metadata=}")

# Tool calling
class GetWeather(BaseModel):
    '''Get the current weather in a given location'''

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


class GetPopulation(BaseModel):
    '''Get the current population in a given location'''

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


# model_with_tools = model.bind_tools([GetWeather, GetPopulation])
# ai_msg = model_with_tools.invoke("Which city is hotter today and which is bigger: LA or NY?")
# print(f"{ai_msg.tool_calls=}")
# >> ai_msg.tool_calls=[{'name': 'GetWeather', 'args': {'location': 'Los Angeles, CA'}, 'id': 'call_00_Iim2trwxyrvjKFveZaNcWuU7', 'type': 'tool_call'}]
# ai_msg.tool_calls

# Structured output
class Joke(BaseModel):
    '''Joke to tell user.'''

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: int | None = Field(description="How funny the joke is, from 1 to 10")


structured_model = model.with_structured_output(Joke)
print(structured_model.invoke("Tell me a joke about cats"))
