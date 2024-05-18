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
