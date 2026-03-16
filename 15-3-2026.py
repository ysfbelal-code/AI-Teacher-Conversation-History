from groq_api import generate_response
import streamlit as st
from languages import languages

if 'language' not in st.session_state:
    st.session_state['language'] = 'English'
language = st.session_state['language']

title_prompt = f"""Only output this header - NOTHING else. 
It's crucial you musn't change ANYTHING, otherwise it will cause confusion among users. 
Translate the heading to {language} if language isn't English. 
Don't change ANYTHING from the text either and AVOID repetition at all costs."""

st.set_page_config(page_title=generate_response(title_prompt + "AI MATH MASTERMIND"), layout='centered')
st.session_state.setdefault('conversation', [])

st.markdown("""
<style>
@import url('');

html, body, [class*="css"], [class*="st-"], .stApp, .stApp * {
    font-family: 'Yu Gothic UI Light', Yu, sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

language = st.sidebar.selectbox("Choose the app language:", list(languages.keys()))
if language:
    st.session_state['language'] = language

st.title(generate_response(title_prompt + "MATH WIZARD"), text_alignment='center')

c1, c2, c3 = st.columns([1,1,1])
with c1:
    view = st.button(generate_response(title_prompt + ("View conversation history")))
with c2:
    clear = st.button(generate_response(title_prompt + "Clear conversation history"))
with c3:
    export = st.button(generate_response(title_prompt + ("Export conversation history")))
    
difficulty = st.selectbox(generate_response(title_prompt + "Which grade are you? This will determine the difficulty of the questions:"), 
                          (generate_response(title_prompt + "Primary/Elementary"), generate_response(title_prompt + "Secondary/Middle School"), 
                           generate_response(title_prompt + "6th Form/High School"), generate_response(title_prompt + "University")))

user_question = st.text_input(generate_response(title_prompt + "How can I help you today?"))
solve = st.button(generate_response(title_prompt + "Solve"))
if solve:
    prompt = f"""
    You are a math wizard helping a {difficulty} student solve a difficult question. 
    Be comprehensive and helpful with your explanations, and don't change the subject. 
    Do NOT include any profanity whatsoever, this program is used by students.
    Answer this question: {user_question}
    Translate the answer into {language}."""
    st.markdown(generate_response(prompt))
