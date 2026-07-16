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
from langgraph.checkpoint.memory import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_comminity.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

from dotenv import load_dotenv
import sqlite3
import requests

load_dotenv()


# -----------------------------
# 1. LLM
llm = ChatOpenAI()

# -----------------------------
# 2. Tools
# Tools
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "subtract":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                raise {"error": "Division by zero is not allowed."}
            result = first_num / second_num
        else:
            raise {"error": f"Unsupported operation: {operation}"}
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        raise {"error": str(e)}


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

SERVERS = {
    "github": {
        "transport": "stdio",
        "command": "/usr/bin/python3",
        "args": [
            "/path/to/github_mcp_server.py"
        ]
    }
}

# Make tool list
tools = [get_stock_price, calculator, search_tool]

# make the LLM tool-aware
llm_with_tools = llm.bind_tools(tools)


# --------------------------
# 3. State

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# -------------------------------
# 4. Nodes

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools) # Executes tool calls


# -------------------------------
# 5. Checkpointer

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver()

# -------------------------------
# 6. Graph
# -------------------------------
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node('tools', tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer = checkpointer)


# ---------------------
# 7. Helper
# ---------------------
def retrieve_all_threads():
    all_threads = set()

    for checkpointer in checkpointer.list(None):
        all_threads.add(checkpointer.config['configurable']['thread_id'])

    print(list(all_threads))
    return list(all_threads)


