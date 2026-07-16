from langgraph.graph import StateGraph, START
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_comminity.tools import DuckDuckGoSearchRun
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
import asyncio
# library for addition of mcp
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables from .env file
load_dotenv() 

llm = ChatOpenAI(model="gpt-5")

# MCP client for local FastMCP server
client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio", # as local mcp server so stdio
            "command": "python3",
            "args": ["./mcp_server.py"] # path to the server file
        },
        "expense": {
            "tranport": "streamable_http", # if this fails try sse
            "url": "https://splendid-gold-dingo.fastmcp.app/mcp"
        }
    }
)


# # Make tool list
# tools = [calculator]

# # make the LLM tool-aware
# llm_with_tools = llm.bind_tools(tools)

# State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

async def build_graph():

    tools = await client.get_tools()
    print(tools)
    llm_with_tools = llm.bind_tools(tools)
    # Nodes
    async def chat_node(state: ChatState):
        messages = state['messages']
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    # Executes tool calls
    tool_node = ToolNode(tools) 

    # Graph
    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_node('tools', tool_node)

    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges('chat_node', tools_condition)
    graph.add_edge("tools", "chat_node")

    chatbot = graph.compile()
    return chatbot

async def main():
    chatbot = await build_graph()

    # running the graph
    # 1st question - Calculate modulus of 35 and 4
    result = await chatbot.ainvoke({"messages": [HumanMessage(content="Add an expense - Rs. 500/- to the Udemy course.")]})
    # try different questions
    
    print(result['message'][-1].content)

if __name__ == '__main__':
    asyncio.run(main())