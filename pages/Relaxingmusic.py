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
import streamlit as st # import tensorflow_datasets as tfds
from animations import load
from random import randrange as rr

dog= "animations/dog animation.json"

flow= "animations/floating person.json"

neko = "animations/neko animation.json"

windmill= "animations/windmill.json"

guy= "animations/guy relaxing.json"

ls= [dog,flow,neko,windmill,guy]

i=rr(0,4)
load(ls[i])



if "sound" not in st.session_state:
    st.session_state.sound = "sounds/relaxing sounds.m4a"

def changesong():
    if st.session_state.pre=="Relaxing Sounds":
        st.session_state.sound="sounds/relaxing sounds.m4a"
    elif st.session_state.pre=="Really Calming Sounds":
        st.session_state.sound="sounds/Calming sounds.mp3"
    elif st.session_state.pre=="Guitar Music":
        st.session_state.sound="sounds/Guitar music.mp3"
    elif st.session_state.pre=="Ocean Music":
        st.session_state.sound="sounds/Guitar sounds.mp3"


st.selectbox("Select a song",options=["Relaxing Sounds","Really Calming Sounds","Guitar Music","Ocean Music"],key="pre",on_change=changesong)
st.audio(st.session_state.sound)


col1,col2,col3=st.columns(3)
with col1:
    st.page_link('app.py',label='Chat',icon='💬',help='Chat with pandora your theurapathic ai mental assistant your thoughts will be organized here')
with col2:
    st.page_link('pages/Journal.py',label='Journal',icon='📖',help='Write your thoughts in a journal')

with col3:
    st.page_link('pages/Relaxingmusic.py',label='Relaxing Music',icon='🎶',help='Listen to relaxing music to cool your mind')



