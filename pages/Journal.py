import streamlit as st
from pymongo import MongoClient
from pymodm import connect, MongoModel, fields
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')


if "sound" not in st.session_state:
    st.session_state.sound = "sounds/relaxing sounds.m4a"


connect(MONGO_URI)
if "history_ids" not in st.session_state:
    st.session_state.history_ids=None

if "user_details" not in st.session_state:
    try:
        st.session_state.user_details=st.session_state.UD._id
    except:
        st.switch_page("app.py")

class User(MongoModel):
    user_name = fields.CharField(mongo_name="User Name")
    first_name = fields.CharField(mongo_name="First Name")
    last_name = fields.CharField(mongo_name="Last Name")
    password = fields.CharField(mongo_name="Password")
    user_number = fields.CharField(mongo_name="User Phone Number")
    trustee_number = fields.CharField(mongo_name="Truste Phone Number")
    user_email = fields.CharField(mongo_name="User Email")
    trustee_email = fields.CharField(mongo_name="Trustee Email")

class History(MongoModel):
    UserDetails = fields.ReferenceField(User, mongo_name="User Details")
    journal = fields.CharField(mongo_name="Journal")

def save_note(note, _user_id,_note_id=None):
    client = MongoClient(MONGO_URI)
    db = client.mentalhealthdb
    notes = db.history
    if _note_id is None:
        result = notes.insert_one({"Journal": note,"User Details":_user_id})
        return str(result.inserted_id)
    else:
        notes.update_one({"_id": _note_id}, {"$set": {"Journal": note}})
        return str(_note_id)

@st.cache_resource
def save_history(_UserDetails: ObjectId, journal):
    history_id = history_ID_query(_UserDetails)

    if history_id == []:
        new_history = History(UserDetails=_UserDetails, journal=journal)
        new_history.save()
        print("Saved")
        return new_history
    else:
        History.objects.raw({'_id': history_id[0]}).update(
            {"$set": {"journal": journal}}, upsert=True)
        return History.objects.get(_id=history_id[0])

def get_journal_by_history_id(history_id):
    history_doc = History.objects.get(_id=history_id)

    if history_doc:
        journal_content = history_doc.journal
        return journal_content
    else:
        return None
    
def get_history_id_by_journal(journal):
    client = MongoClient(MONGO_URI)
    db = client.mentalhealthdb
    notes = db.history
    return notes.find_one({"Journal": journal})['_id']

def history_ID_query(_UserDetails: ObjectId) -> list:
    history_entries = History.objects.raw({'UserDetails': _UserDetails})
    history_ids = []

    try:
        for entry in history_entries:
            history_ids.append(entry._id)
    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return []

    return history_ids


def get_notes(user_details):
    client = MongoClient(MONGO_URI)
    db = client.mentalhealthdb
    notes = db.history
    return notes.find({"User Details": user_details})

st.title("Journal")

if 'text' not in st.session_state:
    st.session_state.text=''

if 'notes_history' not in st.session_state:
    st.session_state.notes_history=[]
    for notes in get_notes(st.session_state.user_details):
            st.session_state.notes_history.append( notes['Journal'])





def change():
    st.session_state.text=st.session_state.selected_note
    st.session_state.notes_history=[]
    for notes in get_notes(st.session_state.user_details):
        st.session_state.notes_history.append( notes['Journal'])



































st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)



    





if "user_logged" not in st.session_state:
    st.session_state.user_logged = False


if st.session_state.user_logged == False:
    st.switch_page('pages/login.py')


textinput,Music = st.tabs(["Write or edit your text for your journal", "Listen to relaxing music"])


with textinput:
    # Display the text area with the saved value from session state
    
    st.session_state.text=st.text_area(label='Write your thoughts in this safe space', key="thoughts",value=st.session_state.text)
    col1,col2=st.columns(2)
    
    with col1:
        if st.button("Save as a new Note",type='primary'):
            save_history(st.session_state.user_details, st.session_state.thoughts)
            st.session_state.history_ids = history_ID_query(st.session_state.user_details)
            st.write("Note saved!")
            st.session_state.notes_history=[]
            for notes in get_notes(st.session_state.user_details):
                st.session_state.notes_history.append( notes['Journal'])
            
            st.rerun()
        
    with col2:
        selected = st.selectbox("Select a note",placeholder="Select a note to update",options=st.session_state.notes_history,on_change=change,key="selected_note")
       
        selected_note = get_history_id_by_journal(selected)

        st.write(selected_note)



        if st.button("Update Note"):
            print(save_note(st.session_state.thoughts,st.session_state.user_details, _note_id=selected_note))
            
            st.write("Note updated!")
            st.session_state.notes_history=[]
            for notes in get_notes(st.session_state.user_details):
                st.session_state.notes_history.append( notes['Journal'])
            st.rerun()
        


    st.write("# You wrote")
    st.write(st.session_state.thoughts)






with Music:
    import streamlit as st 
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








# st.rerun()
