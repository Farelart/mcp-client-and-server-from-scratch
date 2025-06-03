from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools

from langgraph.prebuilt import create_react_agent

from langchain_groq import ChatGroq

import asyncio

import os

GROQ_API_KEY = "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"

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

model = ChatGroq(model="llama3-8b-8192", temperature=0)

# Ensure the parent directory exists
parent_directory = "C:\\Users\\User\\Documents\\mcp-client-and-server-from-scratch"
os.makedirs(parent_directory, exist_ok=True)

# Define your working directory
directory = os.path.join(parent_directory, "filesystem-mcp-client")
os.makedirs(directory, exist_ok=True)

# Configure the filesystem server with a working directory that exists
server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        directory
    ],
    cwd=directory
)

""" async def run_agent():
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
 """

async def run_file_operations():
    process = None  # Keep track of the process
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:

                await session.initialize()

                print("MCP Session Initialized.")
                
                tools = await load_mcp_tools(session)
                
                print(f"Loaded Tools: {[tool.name for tool in tools]}")
                
                list_dir_tool = next((tool for tool in tools if tool.name == "list_directory"), None)
                
                if list_dir_tool:
                    files = await list_dir_tool.ainvoke({"path": directory})
                    print("Current directory contents:")
                    print(files)
                
                agent = create_react_agent(model, tools)

                print("ReAct Agent Created.")

                query = input("ask me something")

                response = await agent.ainvoke({

                    "messages": [("user", query)]

                })

                print(response)

                return response["messages"][-1].content
                    
    except Exception as e:
        print(f"An error occurred: {type(e).__name__}: {str(e)}")
        if hasattr(e, 'exceptions'): # For ExceptionGroup
            for i, sub_ex in enumerate(e.exceptions):
                print(f"  Sub-exception {i+1}: {type(sub_ex).__name__}: {str(sub_ex)}")

    finally:
        await asyncio.sleep(0.1)
        print("Client script finished.")


if __name__ == "__main__":

    print("Starting MCP Client...")

    result = asyncio.run(run_file_operations())

    print("\nAgent Final Response:")
    
    print(result)

""" if __name__ == "__main__":

    print("Starting MCP Client...")

    result = asyncio.run(run_agent())

    print("\nAgent Final Response:")
    
    print(result)
 """
