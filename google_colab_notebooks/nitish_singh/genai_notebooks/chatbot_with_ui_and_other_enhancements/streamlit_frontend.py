import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage


# st.session_state -> dict -> this resets only when user refreshes page, otherwise it will keep accumulating all messages, without it, normal list like below message_history with each user_input full script will be rerun again, with no saving of chat history

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# message_history = []

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#with st.chat_message('user'):
 #   st.text('hi')

#with st.chat_message('assistant'):
 #   st.text('How can i help you?')

#with st.chat_message('user'):
 #   st.text('My name is Koyel')

user_input = st.chat_input('Type here')

if user_input:

    # first add the new message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message = response['messages'][-1].content
                   
    # secondly add the new message to message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)


