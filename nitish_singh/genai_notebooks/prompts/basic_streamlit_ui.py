import streamlit as st

st.header('Research Tool')

user_input = st.text_input('Enter your prompt')

if st.button('Summarize'):
    st.text('Some random text')