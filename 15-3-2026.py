from groq_api import generate_response
import streamlit as st
from languages import languages

st.session_state.setdefault('conversation', [])
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

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

title_prompt = f"This is just a heading. Only output this, and NOTHING else. You musn't change anything, otherwise it will cause confusion among users. Translate the heading to {language}."

st.set_page_config(page_title=generate_response(title_prompt + "AI MATH MASTERMIND"), layout='centered')
st.title(generate_response(title_prompt + "MATH WIZARD"), text_alignment='center')
difficulty = st.selectbox(generate_response(title_prompt + "Which grade are you? This will determine the difficulty of the questions:"), 
                          (generate_response(title_prompt + "Primary/Elementary"), generate_response(title_prompt + "Secondary/Middle School"), 
                           generate_response(title_prompt + "6th Form/High School"), generate_response(title_prompt + "University")))

user_question = st.text_input(generate_response(title_prompt + "How can I help you today?"))
if user_question:
    prompt = f"""
    You are a math wizard helping a {difficulty} student solve a difficult question. 
    Be comprehensive and helpful with your explanations, and don't change the subject. 
    Do NOT include any profanity whatsoever, this program is used by students.
    Answer this question: {user_question}
    Translate the answer into {language}."""
    st.markdown(generate_response(prompt))
