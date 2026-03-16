from groq_api import generate_response
import streamlit as st
from languages import languages

language = st.sidebar.selectbox("Choose the app language:", list(languages.keys()))
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'
if language != st.session_state.get('prev_language'):
    st.cache_data.clear()
    st.session_state['prev_language'] = language
if language:
    st.session_state['language'] = language

title_prompt = f"""Only output this title - NOTHING else. 
It's crucial you musn't change ANYTHING, otherwise it will cause confusion among users. 
Translate the heading to {st.session_state['language']} if language isn't English. 
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

title = generate_response(title_prompt + "MATH WIZARD")
header = generate_response(title_prompt + ("View conversation history"))
header2 = generate_response(title_prompt + ("Clear conversation history"))
header3 = generate_response(title_prompt + ("Export conversation history"))

st.title(title, text_alignment='center')
c1, c2, c3 = st.columns([1,1,1])
with c1:
    view = st.button(header)
with c2:
    clear = st.button(header2)
with c3:
    export = st.button(header3)

grade = generate_response(title_prompt + "Which grade are you? This will determine the difficulty of the questions:")
choice = generate_response(title_prompt + "Primary/Elementary")
choice2 = generate_response(title_prompt + "Secondary/Middle School")
choice3 = generate_response(title_prompt + "6th Form/High School")
choice4 = generate_response(title_prompt + "University")
help = generate_response(title_prompt + "How can I help you today?")
solve = generate_response(title_prompt + "Solve")

difficulty = st.selectbox(grade, (choice, choice2, choice3, choice4))
user_question = st.text_input(help)
solve = st.button(solve)

if solve:
    prompt = f"""
    You are a math wizard helping a {difficulty} student solve a difficult question. 
    Be comprehensive and helpful with your explanations, and don't change the subject. 
    Do NOT include any profanity whatsoever, this program is used by students.
    Answer this question: {user_question}
    Translate the answer into {language}."""
    answer = generate_response(prompt)
    st.markdown(answer)
