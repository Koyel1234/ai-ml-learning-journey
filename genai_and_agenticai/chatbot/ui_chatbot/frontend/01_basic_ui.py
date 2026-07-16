# in this and backend scripts we divided last built chatbot and then improve that 

import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

with st.chat_message('user'):
   st.text('hi')

with st.chat_message('assistant'):
   st.text('How can i help you?')

with st.chat_message('user'):
   st.text('My name is Koyel')


