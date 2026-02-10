import asyncio

from mcp import ClientSession
from mcp import StdioServerParameters
from mcp import stdio_client

# 为stdio连接创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里是python
    command="python",
    # 启动命令的附加参数，这里是运行example_server.py
    args=["05_mcp_server.py"],
    # 环境变量，默认为None,表示使用当前环境变量
    env=None
)


# 或者使用 配置
# {
#     "mcpServers": {
#         "calculator": {
#         "command": "python",
#         "args": ["calculatorMCPServer.py"],
#         "env": null,
#         },
#         "amap-maps": {
#             "command": "npx",
#             "args": ["-y", "@amap/amap-maps-mcp-server"],
#             "env":{
#                 "АМАР_MAPS_API_KEY": "${AMAP_MAPS_API_KEY}"
#             }
#         }
#     }
# }

# 服务器端功能测试
async def run():
    # 创建与服务器的标准输入/输出连接，并返回reαd和write流
    async with stdio_client(server_params) as (read, write):
        # 创建一个客户端会话对象，通过read和write流与服务器交互
        async with ClientSession(read, write) as session:
            # 向服务器发送初始化请求，确保连接准备就绪
            # 建立初始状态，并让服务器返回其功能和版本信息
            capabilities = await session.initialize()
            print(f"Supported capabilities:{capabilities.capabilities}/n/n")
            # 请求服务器列出所有支持的t00LS
            tools = await session.list_tools()
            print(f"Supported tools:{tools}/n/n")
            # 文件相关功能测试
            add_result = await session.call_tool("add", arguments={"a": 6, "b": 3})
            subtract_result = await session.call_tool("subtract", arguments={"a": 6, "b": 3})
            multiply_result = await session.call_tool("multiply", arguments={"a": 6, "b": 3})
            divide_result = await session.call_tool("divide", arguments={"a": 6, "b": 3})
            print(f"add_result:{add_result}/n/n")
            print(f"subtract_result:{subtract_result}/n/n")
            print(f"multiply_result:{multiply_result}/n/n")
            print(f"divide_result:{divide_result}/n/n")


if __name__ == "__main__":
    asyncio.run(run())

"""
现在要购买一批货,单价是1034.32423,数量是235326。商家后来又说,可以在这个基础上,打95折,折后总价是多少?
我和商家关系比较好,商家说,可以在上面的基础上,再返回两个点,最后总价是多少?
"""
