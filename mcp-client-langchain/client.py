from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools

from langgraph.prebuilt import create_react_agent

from langchain_groq import ChatGroq

import asyncio

import os

""" from langchain_openai import ChatOpenAI """


GROQ_API_KEY = "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"

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

model = ChatGroq(model="llama3-8b-8192", temperature=0)

server_params = StdioServerParameters(
    command="python",
    args=["server.py"]
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            print("MCP Session Initialized.")

            tools = await load_mcp_tools(session)

            print(f"Loaded Tools : {[tool.name for tool in tools]}")

            agent = create_react_agent(model, tools)

            print("ReAct Agent Created.")

            query = input("ask me something")

            response = await agent.ainvoke({

               "messages": [("user", query)]

           })

            print(response)

            return response["messages"][-1].content



if __name__ == "__main__":

    print("Starting MCP Client...")

    result = asyncio.run(run_agent())

    print("\nAgent Final Response:")
    
    print(result)
