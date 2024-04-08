import streamlit as st
if "UD" not in st.session_state:
    st.session_state.UD = None
from database import db_login_signup


def login():
    st.session_state.UD=db_login_signup(proceed=2,user_name=st.session_state.username_field,password=st.session_state.password_field)
    
    



hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .viewerBadge_link__qRIco{display:None;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "type" not in st.session_state:
    st.session_state.type = "L"

if "stop" not in st.session_state:
    st.session_state.stop = False

LformLayout = st.empty()





        


def loginPage():
    with LformLayout.container(border=True):
        st.title("Login Page")
        st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)
        st.text_input("Enter your username",max_chars=20,key='username_field',help='Maximum of 20 characters')

        
        st.text_input("Enter your password",max_chars=20,key='password_field',type='password',help='Maximum of 20 characters')
        if st.button('Login', type='primary',on_click=login):
            st.session_state.user_logged=True


        if st.button("Create an account", key="login_button"):
            st.session_state.type = "R"
            st.rerun()  # Update session state

# Main logic for page switching


if __name__ =="__main__":
    loginPage()

if st.session_state.type == "R":
    st.switch_page('pages/register.py')


if st.session_state.UD !=None:
    
    st.switch_page('app.py')
    


