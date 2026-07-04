from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt
from dotenv import load_dotenv
load_dotenv()

st.header('Research Tool')

paper_input = st.selectbox(
    'Select research Paper Name',[
        'Attention Is All You Need', 
        'BERT: Pre-training of Deep Bidirectional Transformers', 
        'GPT-3: Language Models are Few-Shot Learners', 
        'Diffusion Models beat GANs on Image Synthesis'
])

style_input = st.selectbox(
    'Select Explanation Style',[
        'Beginner-Friendly', 
        'Technical', 
        'Code-Oriented', 
        'Mathematical'
])

length_input = st.selectbox('Select Explanation Length',[
    'Short (1-2 paragraphs)',
    'Medium (3-5 paragraphs)',
    'Long (detailed explanation)'
])


# load prompt from template.json file instead of writing here
template = load_prompt('template.json')

prompt = template.invoke({
    'paper_input': paper_input,
    'style_input': style_input,
    'length_input': length_input
})

model = ChatOpenAI(model = "gpt-4", temperature = 0)


if st.button('Summarize'):
    result = model.invoke(prompt)
    st.write(result.content)