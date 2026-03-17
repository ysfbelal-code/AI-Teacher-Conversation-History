from groq_api import generate_response
import streamlit as st
from languages import languages
import io

st.set_page_config(page_title="AI MATH MASTERMIND", layout='centered')
st.session_state.setdefault('conversation', [])

language = st.sidebar.selectbox("Choose the app language:", list(languages.keys()), key='language_select')

rtl = ('Arabic', 'Hebrew', 'Urdu', 'Persian', 'Pashto', 'Sindhi', 'Uyghur', 'Yiddish')

if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

if language != st.session_state.get('prev_language'):
    st.cache_data.clear()
    st.session_state['prev_language'] = language

if language:
    st.session_state['language'] = language

if st.session_state['language'] == "English":
    title_prompt = "Output ONLY the following text, exactly as written. Nothing else. Keep ALL mathematical expressions, variables, numbers, and symbols exactly as they appear in the original.\n"
else:
    title_prompt = f"Translate the following text to {language}. ONLY output the translation, nothing else. Keep ALL mathematical expressions, variables, numbers, and symbols exactly as they appear in the original. Only translate the surrounding text words.\n"

if st.session_state['language'] in rtl:
    st.markdown("""
    <style>
    .stMarkdown p, .stMarkdown li, .stMarkdown pre,
    .stExpander, .stExpander *,
    [data-testid="stExpander"], [data-testid="stExpander"] * {
        direction: rtl !important;
        text-align: left !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
st.markdown("""
<style>
@import url('');

html, body, [class*="css"], [class*="st-"], .stApp, .stApp * {
    font-family: 'Yu Gothic UI Light', Yu, sans-serif !important;
}
            
.stMarkdown p, .stMarkdown  li, .stMarkdown pre {
    font-size: 1.0rem !important;            
}

[data-testid="stIconMaterial"] {
    visibility: hidden;
    position: relative;
}

[data-testid="stIconMaterial"]::before {
    content: '||';
    visibility: visible;
    position: absolute;
    left: 0;
    font-family: monospace;
    font-size: 1rem;
}

[data-testid="stSidebarCollapseButton"] {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

title = generate_response(title_prompt + "MATH WIZARD")
header = generate_response(title_prompt + "View conversation history")
header2 = generate_response(title_prompt + "Clear conversation history")
header3 = generate_response(title_prompt + "Export conversation history")

st.markdown(f"<h1 style='text-align:center'>{title}</h1>", unsafe_allow_html=True)
with st.expander(generate_response(title_prompt + "Examples of problems I can solve:")):
    st.markdown(generate_response(title_prompt + 
"""
Probability - There are 17 counters in a bag,
4 of the counters are red and the rest are blue.
A counter is taken from the bag at random.
Find the probability that the counter is blue

Algebra - Simplify (x-7)(x+9)

Trigonometry - ABC is a right-angled triangle.
The height - AB - is 12cm and the hypotenuse - BC - is 13cm.
Calculate angle x at the base.

Discrete Maths - If a set B has n elements, then what is the total number of subsets of B? Justify your answer.""")
, text_alignment='left' if language not in rtl else 'right')
    
c1, c2, c3 = st.columns([1,1,1])
with c1:
    view = st.button(header, key='view_button')
with c2:
    clear = st.button(header2, key='clear_button')
with c3:
    export = st.button(header3, key='export_button')

grade = generate_response(title_prompt + "Which grade are you? This will determine the AI's answers:")
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
    if st.session_state['conversation'] != []:
        st.session_state['conversation'] = []
        result = generate_response(title_prompt+"Conversation history cleared!")
    else:
        result = generate_response(title_prompt+"Conversation history already empty.")
    st.toast(result)
elif view:
    if st.session_state['conversation'] != []:
        for i, chat in enumerate(st.session_state.conversation, 1):
            result = generate_response(title_prompt + f"Q{i}:\n{chat['question']}\nA{i}:{chat['answer']}\n\n")
        st.markdown(result, text_alignment='left' if language not in rtl else 'right')
    else:
        result = generate_response(title_prompt + "Conversation history empty.")
        st.toast(result)
elif export:
    def export_bytes(history):
        for i, chat in enumerate(st.session_state.conversation, 1):
            text = "".join(f"Q{i}:\n{chat['question']}\nA{i}:{chat['answer']}\n\n")
            return io.BytesIO(text.encode("utf-8"))
    if st.session_state.conversation != []:
        st.download_button(
            label="Export chat history", 
            data = export_bytes(st.session_state.conversation),
            file_name = "AI_Math_Wizard_Conversation_History.txt",
            mime="text/plain"
        )
    else:
        st.toast(generate_response(title_prompt + "Conversation history empty."))
elif solve:
    if user_question.strip():
        prompt = f"""
        You are a math wizard helping a {difficulty} student solve a difficult question. 
        The answers should not be too short, and be comprehensive and helpful with your explanations, and don't change the subject. 
        Do NOT include any profanity whatsoever, this program is used by students.
        Show your methods of working out and include concise diagrams.
        Answer this question: {user_question}"""
        
        with st.spinner("Thinking carefully..."):
            answer = generate_response(prompt)
            st.session_state.conversation.append({'question':user_question.strip(), 'answer':answer})
        st.markdown(answer, text_alignment='left' if language not in rtl else 'right')
    else:
        st.toast(generate_response(title_prompt + "Please enter a question if you want to use this AI."))
