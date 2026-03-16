from groq_api import generate_response
import streamlit as st
from languages import languages

st.set_page_config(page_title="AI MATH MASTERMIND", layout='centered')
st.session_state.setdefault('conversation', [])

language = st.sidebar.selectbox("Choose the app language:", list(languages.keys()), key='language_select')

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

st.markdown("""
<style>
@import url('');

html, body, [class*="css"], [class*="st-"], .stApp, .stApp * {
    font-family: 'Yu Gothic UI Light', Yu, sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

title = generate_response(title_prompt + "MATH WIZARD", language=language)
header = generate_response(title_prompt + "View conversation history", language=language)
header2 = generate_response(title_prompt + "Clear conversation history", language=language)
header3 = generate_response(title_prompt + "Export conversation history", language=language)

st.title(title, text_alignment='center')
c1, c2, c3 = st.columns([1,1,1])
with c1:
    view = st.button(header, key='view_button')
with c2:
    clear = st.button(header2, key='clear_button')
with c3:
    export = st.button(header3, key='export_button')

grade = generate_response(title_prompt + "Which grade are you? This will determine the difficulty of the questions:", language=language)
choice = generate_response(title_prompt + "Primary/Elementary", language=language)
choice2 = generate_response(title_prompt + "Secondary/Middle School", language=language)
choice3 = generate_response(title_prompt + "6th Form/High School", language=language)
choice4 = generate_response(title_prompt + "University", language=language)
help = generate_response(title_prompt + "How can I help you today?", language=language)
solve_question = generate_response(title_prompt + "Solve", language=language)

difficulty = st.selectbox(grade, (choice, choice2, choice3, choice4), key='difficulty_select')
user_question = st.text_input(help, key='question_input')
solve = st.button(solve_question, key='solve_button')

if solve:
    prompt = f"""
    You are a math wizard helping a {difficulty} student solve a difficult question. 
    Be comprehensive and helpful with your explanations, and don't change the subject. 
    Do NOT include any profanity whatsoever, this program is used by students.
    Answer this question: {user_question}"""
    answer = generate_response(prompt, language=language)
    st.markdown(answer)
