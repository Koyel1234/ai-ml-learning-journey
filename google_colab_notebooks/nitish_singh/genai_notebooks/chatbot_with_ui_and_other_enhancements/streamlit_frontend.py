import streamlit as st

with st.chat_message('user'):
    st.text('hi')

with st.chat_message('assistant'):
    st.text('How can i help you?')

with st.chat_message('user'):
    st.text('My name is Koyel')

user_input = st.chat_input('Type here')
