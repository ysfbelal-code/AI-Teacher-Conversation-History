from groq_api import translate_text
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

st.set_page_config(page_title=translate_text("AI MATH MASTERMIND", language), layout='centered')
st.title(translate_text("MATH WIZARD", language), text_alignment='center')
difficulty = st.selectbox(translate_text("Which grade are you? This will determine the difficulty of the questions:", language), 
                          (translate_text("Primary/Elementary", language), translate_text("Secondary/Middle School", language), 
                           translate_text("6th Form/High School", language), translate_text("University", language)))

user_question = st.text_input(translate_text("How can I help you today?", language))
if user_question:
    prompt = f"""
    You are a math wizard helping a {difficulty} student solve a difficult question. 
    Be comprehensive and helpful with your explanations, and don't change the subject. 
    Do NOT include any profanity whatsoever, this program is used by students.
    Answer this question: {user_question}"""
    st.markdown(translate_text(prompt, language))
