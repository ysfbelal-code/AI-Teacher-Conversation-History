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

if st.session_state['language'] == "English":
    title_prompt = "Output ONLY the following text, exactly as written. Nothing else.\n"
else:
    title_prompt = f"Translate the following text to {language}. ONLY output the translation, nothing else.\n"

st.markdown("""
<style>
@import url('');

html, body, [class*="css"], [class*="st-"], .stApp, .stApp * {
    font-family: 'Yu Gothic UI Light', Yu, sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

title = generate_response(title_prompt + "MATH WIZARD")
header = generate_response(title_prompt + "View conversation history")
header2 = generate_response(title_prompt + "Clear conversation history")
header3 = generate_response(title_prompt + "Export conversation history")

st.markdown(f"<h1 style='text-align:center'>{title}</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1,1,1])
with c1:
    view = st.button(header, key='view_button')
with c2:
    clear = st.button(header2, key='clear_button')
with c3:
    export = st.button(header3, key='export_button')

grade = generate_response(title_prompt + "Which grade are you? This will determine the difficulty of the questions:")
choice = generate_response(title_prompt + "Primary/Elementary")
choice2 = generate_response(title_prompt + "Secondary/Middle School")
choice3 = generate_response(title_prompt + "6th Form/High School")
choice4 = generate_response(title_prompt + "University")
help = generate_response(title_prompt + "How can I help you today?")
solve_question = generate_response(title_prompt + "Solve")

difficulty = st.selectbox(grade, (choice, choice2, choice3, choice4), key='difficulty_select')
user_question = st.text_input(help, key='question_input')
solve = st.button(solve_question, key='solve_button')

if clear:
    if st.session_state['conversation'] is not None:
        st.session_state['conversation'] = []
        result = generate_response(title_prompt+"Conversation history cleared!")
    else:
        result = generate_response(title_prompt+"Conversation history already empty.")
    st.toast(result)
elif solve:
    prompt = f"""
    You are a math wizard helping a {difficulty} student solve a difficult question. 
    Be comprehensive and helpful with your explanations, and don't change the subject. 
    Do NOT include any profanity whatsoever, this program is used by students.
    Show your methods of working out and include concise diagrams.
    Answer this question: {user_question}"""
    with st.spinner("Thinking carefully..."):
        answer = generate_response(prompt)
    st.markdown(answer)
