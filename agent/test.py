import os

import requests
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


def heweather(location):
    """ Get the weather in a specific location. """
    print("111111111111111111111111")
    url = f"https://devapi.qweather.com/v7/weather/now?location={location}"
    response = requests.get(url)
    print(f"{response=}")
    return response.json()


# Tool calling
class GetWeather(BaseModel):
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


class GetPopulation(BaseModel):
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


model_with_tools = model.bind_tools([heweather, GetPopulation])
ai_msg = model_with_tools.invoke("上海今天天气怎么样?")
print(f"{ai_msg.content=}")
print(f"{ai_msg.tool_calls=}")
print(f"{ai_msg.usage_metadata=}")
print(f"{ai_msg.response_metadata=}")
# >> ai_msg.tool_calls=[{'name': 'GetWeather', 'args': {'location': 'Los Angeles, CA'}, 'id': 'call_00_Iim2trwxyrvjKFveZaNcWuU7', 'type': 'tool_call'}]
# ai_msg.tool_calls
