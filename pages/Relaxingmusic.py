import streamlit as st
import requests
from openai import OpenAI
import os
from io import BytesIO
import yagmail
st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)


if "user_logged" not in st.session_state:
    st.session_state.user_logged = False


if st.session_state.user_logged == False:
    st.switch_page('pages/login.py')



# Generate a 440 Hz sine wave
note_la = "https://upload.wikimedia.org/wikipedia/commons/c/c4/Muriel-Nguyen-Xuan-Chopin-valse-opus64-1.ogg"
st.audio(note_la,loop=True)

col1,col2,col3=st.columns(3)
with col1:
    st.page_link('app.py',label='Chat',icon='💬',help='Chat with pandora your theurapathic ai mental assistant your thoughts will be organized here')
with col2:
    st.page_link('pages/Journal.py',label='Journal',icon='📖',help='Write your thoughts in a journal')

with col3:
    st.page_link('pages/Relaxingmusic.py',label='Relaxing Music',icon='🎶',help='Listen to relaxing music to cool your mind')



