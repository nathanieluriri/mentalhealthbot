import streamlit as st
import requests
from openai import OpenAI
import os
from io import BytesIO
import yagmail
from moodtracker import moodtrackingsetup


if "user_logged" not in st.session_state:
    st.session_state.user_logged = False


if st.session_state.user_logged == False:
    st.switch_page('pages/login.py')

st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)

if 'moodtrackingsetup' not in st.session_state:
    st.session_state.moodtrackingsetup = moodtrackingsetup




if 'user_name' not in st.session_state:
    st.session_state.user_name = f"{st.session_state.UD.first_name} {st.session_state.UD.last_name}"
if 'user_phone_number'not in st.session_state:
    st.session_state.user_phone_number =st.session_state.UD.user_number 

if 'user_next_of_kin_email' not in st.session_state:
    st.session_state.user_next_of_kin_email = st.session_state.UD.trustee_email.lower() 

if 'user_next_of_kin_phone_number' not in st.session_state:
    st.session_state.user_next_of_kin_phone_number= st.session_state.UD.trustee_number 




# Email account credentials for Hostinger SMTP server


smtp_user = 'mentalhealthbot@247privatesecurity.co.uk'
smtp_password = 'Password10!'

# SMTP server details for Hostinger
smtp_host = 'smtp.hostinger.com'
smtp_port = 465  # Hostinger typically uses port 465 for SMTP with SSL/TLS encryption

# Email content

if 'email_subject' not in st.session_state:
    st.session_state.email_subject = 'Immediate Attention Required: Concern for A Patients Well-being'
if 'email_body' not in st.session_state:
    st.session_state.email_body = f"""

    Dear Health agency,

    I am writing to express concern about {st.session_state.user_name} recent distress, conversations are indicating critical unhappiness. His/her well-being should become your priority.

    It has  come to our attention that he/she  may be in need of self-harm preventive measures. 

    We urge you to reach out to  {st.session_state.user_name} at the following phone number: {st.session_state.user_phone_number} his trustee's email is {st.session_state.user_next_of_kin_email} phone Number for the trustee {st.session_state.user_next_of_kin_phone_number} .

    """

if 'Trustee_email_body' not in st.session_state:
    st.session_state.Trustee_email_body=f"""
Dear Trustee,

I am reaching out to express concern about the recent distress of {st.session_state.user_name} . Recent conversations indicate a state of critical unhappiness, and it is imperative that his/her well-being becomes our top priority.

It has come to our attention that {st.session_state.user_name}  may be in need of preventive measures against self-harm.

We strongly urge you to get in touch with {st.session_state.user_name}  at the following phone number: {st.session_state.user_phone_number}.


"""
# Recipient email address

if 'to_email' not in st.session_state:
    st.session_state.to_email = 'uririnathaniel@gmail.com'

if 'mood' not in st.session_state:
    st.session_state.mood=0



# if mood gets badd mood will be == 14 so an email will be sent
if st.session_state.mood >=10:
    # Create yagmail.SMTP object within a with statement
    with yagmail.SMTP(smtp_user, smtp_password, host=smtp_host, port=smtp_port) as yag:
        # Send the email
        yag.send(to=st.session_state.to_email, subject=st.session_state.email_subject, contents=st.session_state.email_body)
        print('Email sent to the mental health agency successfully!')

        yag.send(to=st.session_state.user_next_of_kin_email, subject=st.session_state.email_subject, contents=st.session_state.Trustee_email_body)
        print('Email sent to the Trustee successfully!')




# Avatar Image object for the ai assistants responses
with open('logo for cloud.png',mode='rb')as image:
    avatarImage = BytesIO(image.read())




def display_previous_chats():
    """
    This function displays the previous chat after every rerun because of how session states work
    """
    for message in st.session_state.messages:
        if message['role']=='assistant':
            with st.chat_message('assistant',avatar=avatarImage):
                st.markdown(message["content"])
        elif message['role']=='user':
            with st.chat_message('user'):
                st.markdown(message["content"])
   

if "messages" not in st.session_state:
    st.session_state.messages = []
else:
    display_previous_chats()


client = OpenAI()

def moodtracking(client)->int:
    mood = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.moodtrackingsetup,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return int(mood.choices[0].message.content)




st.chat_input("hello dear",key="user_input")


def save_chat(role,content):
    """
    This function takes the role and the content the role used and appends it to a list
    """
    if role == "user":
        st.session_state.messages.append({"role":"user","content":content})
        st.session_state.moodtrackingsetup.append({"role":"user","content":content})
        
        

    elif role == "assistant":
        st.session_state.messages.append({"role":"assistant","content":content})
        mood = moodtracking(client=client)
        st.session_state.moodtrackingsetup.append({"role":"assistant","content":f"{mood}"})
        st.session_state.mood+=mood
        print("what",st.session_state.mood,"Mood",mood)

        



@st.cache_data(ttl=30,show_spinner=True)
def assistants_response(user_input:str,messagess)->str:
    
    """
    THIS FUNCTION  RETURNS THE STRING (BOT'S  RESPONSE TO A PROBLEM)
    REQUIRED FOR THE AI TO REPLY WITH
    """
    if len(messagess)==0: 
        completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:group-c::92N3kTla",
        messages=[
        {"role": "system", "content": "You are Pandora, a Personal Therapeutic AI Assistant"},
        {"role": "user", "content": f"{user_input}"}
        ]
        )
        return completion.choices[0].message.content
        
        
    elif len(messagess)>0:
        messages= [ {"role": "system", "content": "You are Pandora, a Personal Therapeutic AI Assistant"}]
        for message in messagess:
            messages.append({"role":f'{message["role"]}', "content": f'{message["content"]}'})
        
        completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:group-c::92N3kTla",
        messages=messages
        )    
        return completion.choices[0].message.content    

        
    
    


if st.session_state.user_input == None:
    pass

else:

    with st.chat_message('user'):

        st.write(st.session_state.user_input)
       
        save_chat("user",st.session_state.user_input)

    with st.chat_message('assistant',avatar=avatarImage):
        

        try:
            st.session_state.bots_reply=assistants_response(st.session_state.user_input,st.session_state.messages)
            st.write(st.session_state.bots_reply)
            
            save_chat("assistant",st.session_state.bots_reply)

        except Exception as e:
            st.write(f"An error occurred:{e}")


    

col1,col2,col3=st.columns(3)
with col1:
    st.page_link('app.py',label='Chat',icon='💬',help='Chat with pandora your theurapathic ai mental assistant your thoughts will be organized here')
with col2:
    st.page_link('pages/Journal.py',label='Journal',icon='📖',help='Write your thoughts in a journal')

with col3:
    st.page_link('pages/Relaxingmusic.py',label='Relaxing Music',icon='🎶',help='Listen to relaxing music to cool your mind')








