#-> create new frontend and backend files
#-> install https://pypi.org/project/langgraph-checkpoint-sqlite/
#-> implement database in backend
#-> chat in multiple threads
#-> install and visualize
#-> integrate to frontend








from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_comminity.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool, BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import aiosqlite
import requests
import asyncio
import threading

load_dotenv()


# Dedicated async loop for backend tasks
_ASYNC_LOOP = asyncio.new_event_loop()
_ASYNC_THREAD = threading.Thread(target=_ASYNC_LOOP.run_forever, daemon=True)
_ASYNC_THREAD.start()


def _submit_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, _ASYNC_LOOP)

def run_async(coro):
    return _submit_async(coro).result()

def submit_async_task(coro):
    """Schedule a coroutine on the backend event loop."""
    return _submit_async(coro)

# -----------------------------
# 1. LLM
llm = ChatOpenAI()

# -----------------------------
# 2. Tools
# Tools
search_tool = DuckDuckGoSearchRun(region="us-en")

# @tool
# def calculator(first_num: float, second_num: float, operation: str) -> dict:
#     """
#     Perform a basic arithmetic operation on two numbers.
#     Supported operations: add, sub, mul, div
#     """
#     try:
#         if operation == "add":
#             result = first_num + second_num
#         elif operation == "subtract":
#             result = first_num - second_num
#         elif operation == "mul":
#             result = first_num * second_num
#         elif operation == "div":
#             if second_num == 0:
#                 raise {"error": "Division by zero is not allowed."}
#             result = first_num / second_num
#         else:
#             raise {"error": f"Unsupported operation: {operation}"}
#         return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
#     except Exception as e:
#         raise {"error": str(e)}


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol )e.g. - 'AAPL', 'TSLA')
    using Alpha Vantage API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=demo" # put my own API key instead of `demo` without quotes
    response = requests.get(url) 
    return response.json()  # returns the JSON response from the API

# @tool
# def list_github_prs(owner: str, repo: str, state: str = "open", per_page: int = 5):
#     """
#     List the latest pull requests for a GitHub repository.

#     Args:
#         owner: GitHuborg or username (e.g. "langgraph-ai")
#         repo: Repository name (e.g. "langgraph")
#         state: "open", "closed0" or "all"
#         per_page: Number of PRs to fetch (max 100)

#     Returns:
#         A simplified list of PR info dictionaries.
#     """
#     token = os.getenv("GITHUB_TOKEN") # optional, for higher rate limits
#     headers = {
#         "Accept": "application/vnd.github+json",
#     }
#     if token:
#         headers["Authorization"] = f"Bearer {token}"
#     url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
#     params = {
#         "state": state,
#         "per_page": per_page
#     }
#     response = requests.get(url, headers = headers, params= params, timeout=10)

#     # assumes GitHun always returns valid JSON with a list of PR objects
#     response.raise_for_status()
#     data = response.json()

#     # Assumes these keys ("number", "title", "user", "state", "html_url") exists
#     prs = []
#     for pr in data:
#         prs.append(
#             {
#                 "number": pr["number"],
#                 "title": pr["title"],
#                 "author": pr["user"]["login"],
#                 "state": pr["state"],
#                 "url": pr["html_url"]
#             }
#         )
    
#     return prs

# SERVERS = {
#     "github": {
#         "transport": "stdio",
#         "command": "/usr/bin/python3",
#         "args": [
#             "/path/to/github_mcp_server.py"
#         ]
#     }
# }

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

def load_mcp_tools() -> list(BaseTool):
    try:
        return run_async(client.get_tools())
    except Exception:
        return []
    
mcp_tools = load_mcp_tools()

# Make tool list
tools = [get_stock_price, search_tool, *mcp_tools]

# make the LLM tool-aware
llm_with_tools = llm.bind_tools(tools) if tools else llm


# --------------------------
# 3. State

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# -------------------------------
# 4. Nodes

async def chat_node(state: ChatState):
    """LLM node that may answer or request a toll call."""
    messages = state['messages']
    response = await llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Executes tool calls
tool_node = ToolNode(tools) if tools else None


# -------------------------------
# 5. Checkpointer

# conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
# checkpointer = SqliteSaver()

async def _init_checkpointer():
    conn = await aiosqlite.connect(database="chatbot.db")
    return AsyncSqliteSaver(conn)

checkpointer = run_async(_init_checkpointer())

# -------------------------------
# 6. Graph
# -------------------------------
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")


if tool_node:
    graph.add_node('tools', tool_node)
    graph.add_conditional_edges('chat_node', tools_condition)
    graph.add_edge("tools", "chat_node")
else:
    graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer = checkpointer)


# ---------------------
# 7. Helper
# ---------------------

async def _alist_threads():
    all_threads = set()

    async for checkpoint in checkpointer.alist(None):
        all_threads.add(checkpointer.config['configurable']['thread_id'])
    return list(all_threads)



def retrieve_all_threads():
    return list(_alist_threads())


