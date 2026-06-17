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
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}


conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer = checkpointer)

#stream = chatbot.stream(
 #       {'messages': [Humanessage(content='What is the recipe to make pasta')]},
  #      config = {'configurable': {'thread_id': 'thread-1'}},
   #     stream_mode = 'messages'
    #    )
#print(type(stream))


# commented out streaming code in langgraph, but for API creation and testing from notebook, this code can be used
#for message_chunk, metadata in chatbot.stream(
 #       {'messages': [Humanessage(content='What is the recipe to make pasta')]},
  #      config = {'configurable': {'thread_id': 'thread-1'}},
   #     stream_mode = 'messages'
    #    ):
    #if message_chunk.content:
     #   print(message_chunk.content, end=" ", flush=True)

#CONFIG = {'configurable': {'thread_id': 'thread-1'}}
#
#response = chatbot.invoke(
#        {'messages': [HumanMessage(content='Hi my name is Koyel')]},
#        config= CONFIG
#        )
#print(chatbot.get_state(config=CONFIG).values['messages'])


# CONFIG = {'configurable': {'thread_id': 'thread-1'}}
# response = chatbot.invoke(
#        {'messages': [HumanMessage(content='Hi my name is Koyel')]},
#        config= CONFIG
#        )
# print(response)

# print(checkpointer.list(None))


def retrieve_all_threads():
    all_threads = set()

    for checkpointer in checkpointer.list(None):
        # print(checkpointer)
        # print(checkpointer.config)
        # print(checkpointer.config['configurable']['thread_id'])
        all_threads.add(checkpointer.config['configurable']['thread_id'])

    print(list(all_threads))
    return list(all_threads)


