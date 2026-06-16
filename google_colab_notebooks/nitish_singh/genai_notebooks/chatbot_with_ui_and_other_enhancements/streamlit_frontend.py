import streamlit as st

message_history = []

# loading the conversation history
for message in message_history:
    with st.chat_message(message['role']):
        st.text(message['content'])

with st.chat_message('user'):
    st.text('hi')

with st.chat_message('assistant'):
    st.text('How can i help you?')

with st.chat_message('user'):
    st.text('My name is Koyel')

user_input = st.chat_input('Type here')

if user_input:

    # first add the new message to message_history
    message_history.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)


    # secondly add the new message to message_history
    message_history.append({'role': 'assistant', 'content': user_input})
    with st.chat_message('assistant'):
        st.text(user_input)


