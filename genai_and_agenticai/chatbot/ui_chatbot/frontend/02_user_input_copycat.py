# in this and backend scripts we divided last built chatbot and then improve that 

import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage


user_input = st.chat_input('Type here')

if user_input:
   with st.chat_message('user'):
      st.text(user_input)

   with st.chat_message('assistant'):
      st.text(user_input)