##Steps for Adding Threading in UI
#
#-> add a sidebar with title + A Start Chat Button + A title named 'My Conversation'
#-> generate dynamic thread id and add it to the session 
#-> Diaply the thread id in sidebar
#
#****************************************************************************************
#
#-> add a New Chat button
#-> On click of new chat open a new chat window
#     * generate a new thread_id
#     * save it in session
#     * reset message history
#
#***************************************************************************************
#
#-> create a list to store all thread_ids
#-> Load all the thread ids in the sidebar
#-> convert the side bar text to clickable buttons
#
#***************************************************************************************
#
#-> on click of a particular thread id load that particular conversation







import streamlit as st
from langgraph_backend_database import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid


# ************************************************ Utility Functions ********************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messsages']

def submit_async_task(coro):
    """Schedule a coroutine on the backend event loop."""
    return _submit_async(coro)

# ************************************************** Session Setup ***************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# here if thread id is not generated, this function will generate thread id
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

# if 'chat_threads' not in st.session_state:
#     st.session_state['chat_threads'] = []

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# ************************************************** Sidebar UI **************************************
st.sidebar.title('LangGraph Chatbot')

#st.sidebar.button('New Chat')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversation')

# st.sidebar.text(st.session_state['thread_id'])
for thread_id in st.session_state['chat_threads'][::-1]:
    #st.sidebar.text(thread_id)
    # st.sidebar.button(str(thread_id))
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages


# ************************************************** Main UI *****************************************
# message history format below
# {'role': 'user', 'content': 'Hi'}
# {'role': 'assistant', 'content': 'Hello'}
# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



if user_input:

    # first add the new message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    # CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    CONFIG = {
        'configurable': {'thread_id': st.session_state['thread_id']},
        "metadata": {
            "thread_id": st.session_state['thread_id']
        },
        "run_name": "chatbot_turn"
    }

    # with st.chat_message('assistant'):
    #     ai_message = st.write_stream(
    #             message_chunk.content for message_chunk, metadata in chatbot.stream(
    #                 {'messages': [HumanMessage(content=user_input)]},
    #                 config=CONFIG,
    #                 stream_mode='messages'
    #             )
    #         )

    # Assistant streaming block
    with st.chat_message("assistant"):
        # use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            event_queue: queue.Queue = queue.Queue()

            async def run_stream():
                try:
                    async for message_chunk, metadata in chatbot.astream(
                        {"messages": [HumanMessage(content=user_input)]},
                        config=CONFIG,
                        stream_mode="messages"
                    ):
                        event_queue.put((message_chunk, metadata))
                except Exception as exc:
                    event_queue.put(("error", exc))
                finally:
                    event_queue.put(None)

            submit_async_task(run_stream())
        
        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="Tool finished", state="complete", expanded=False
            )
    
    # Save assistant message
    st.session_state['message_history'].append(
        {'role': 'assistant', 'content': ai_message}
    )