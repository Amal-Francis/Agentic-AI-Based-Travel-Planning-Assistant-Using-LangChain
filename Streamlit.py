import streamlit as st
import os
import time
from dotenv import load_dotenv
load_dotenv()
from Travel_agent import run_agent


st.set_page_config(page_title='TravelAI Pro', page_icon='✈️')
st.markdown("""
       <style>
       .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
       .stChatInput { border-radius: 20px; }
       </style>
       """, unsafe_allow_html=True)

st.title("✈️ Agentic Travel Planner")
st.caption("With Total Cost Estimation")


# side bar

with st.sidebar:
    st.image('https://cdn-icons-png.flaticon.com/512/826/826070.png', width=100)
    st.header("Trip Details")
    days = st.number_input("How many days?", min_value=1, max_value=30, value=3)
    st.info(f"Budgeting for a **{days}-day** trip.")
    if st.button("Clear Chat History"):
        st.session_state.message = []
        st.rerun()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant', "content": "Hi! I'm your travel assistant."}
    ]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User Interaction
if prompt := st.chat_input('EX: show me hotels in Delhi for a 4 day trip'):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', "content": prompt})

    with st.chat_message('assistant'):
        with st.spinner("Thinking..."):
            try:
                enhanced_query = prompt
                response = run_agent(query=enhanced_query)

                if isinstance(response, list) and len(response) > 0:
                    answer = response[0].get('text', str(response[0]))
                else:
                    answer = str(response)

                st.markdown(answer)
                st.session_state.messages.append({'role': 'assistant', 'content': answer})

            except Exception as e:
                st.error(f"Quota error or connection issue. please tyr in 10 seconds.({e})")
