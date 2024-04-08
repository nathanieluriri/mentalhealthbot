import streamlit as st
import requests
from openai import OpenAI
import os
from io import BytesIO
import yagmail

from database import save_history, history_ID_query,get_journal_by_history_id

st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)


if "user_logged" not in st.session_state:
    st.session_state.user_logged = False


if st.session_state.user_logged == False:
    st.switch_page('pages/login.py')

if 'thoughts' not in st.session_state:
    history_id = history_ID_query(st.session_state.UD._id)
    from bson import ObjectId
    try:
        st.session_state.thoughts= f'{get_journal_by_history_id(ObjectId(history_id[0]))}'
    except:
        st.session_state.thoughts=''



textinput,textdisplay = st.tabs(["Write or edit your text for your journal", "Read what you wrote in your journal"])


with textinput:
    # Display the text area with the saved value from session state
    st.session_state.thoughts = st.text_area(label='Write your thoughts in this safe space', value=st.session_state.thoughts)
with textdisplay:
    # Display the text formatted as a markdown from the text area input
    st.write(st.session_state.thoughts)
    save_history(st.session_state.UD._id,journal=st.session_state.thoughts)
    # print(save_history(st.session_state.UD._id,journal=st.session_state.thoughts))




col1,col2,col3=st.columns(3)
with col1:
    st.page_link('app.py',label='Chat',icon='💬',help='Chat with pandora your theurapathic ai mental assistant your thoughts will be organized here')
with col2:
    st.page_link('pages/Journal.py',label='Journal',icon='📖',help='Write your thoughts in a journal')

with col3:
    st.page_link('pages/Relaxingmusic.py',label='Relaxing Music',icon='🎶',help='Listen to relaxing music to cool your mind')

