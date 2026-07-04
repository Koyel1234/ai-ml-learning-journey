from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt
from dotenv import load_dotenv
load_dotenv()

st.header('Research Tool')
model = ChatOpenAI(model = "gpt-4", temperature = 0, max_completion_tokens = 10)
user_input = st.text_input('Some random text')

if st.button('Summarize'):
    result = model.invoke(user_input)
    st.write(result.content)