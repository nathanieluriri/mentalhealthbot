import streamlit as st




def db_login_signup(proceed, user_name, password, first_name='None', last_name='None', user_number='None', trustee_number='None',user_email='None', trustee_email='None'):
    import bcrypt
    from pymongo import MongoClient
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    MONGO_URI = os.getenv('MONGO_URI')
    connect(MONGO_URI)

    class User(MongoModel):
        user_name = fields.CharField(mongo_name="User Name")
        first_name = fields.CharField(mongo_name="First Name")
        last_name = fields.CharField(mongo_name="Last Name") 
        password = fields.CharField(mongo_name="Password")
        user_number = fields.CharField(mongo_name="User Phone Number") 
        trustee_number = fields.CharField(mongo_name="Truste Phone Number") 
        user_email = fields.CharField(mongo_name="User Email") 
        trustee_email = fields.CharField(mongo_name="Trustee Email") 


    def signup(user, passw, first_name=None, last_name=None, user_number=None, trustee_number=None,user_email=None, trustee_email=None):
        hashed_passw = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
        new_user = User(user_name=user, password=hashed_passw, first_name=first_name, last_name=last_name, user_number=user_number, trustee_number=trustee_number,user_email=user_email, trustee_email=trustee_email)
        if first_name !='None' and last_name!='None' and user_number !='None' and trustee_number !='None' and user_email !='None' and trustee_email !='None':
            new_user.save()
        return new_user

    def login(user, passw):
        users = User.objects.all()

        for u in users:
            if user == u.user_name:
                print(f"{user} and {u.user_name}")
                checkP = u.password
                checkP = checkP[2:-1]
                checkP = bytes(checkP, 'utf-8')
                if bcrypt.checkpw(passw.encode('utf-8'), checkP):
                    print('Login successful')
                    return u

        return None

    def check(user_name: str) -> bool:
        users = User.objects.all()
        if users.count() == 0:
            return True
        else:
            for user in users:
                if user_name == user.user_name:
                    # User name found in the database
                    return False
            # User name not found in the database
            return True
    def start(process,user_name, password, first_name=None, last_name=None, user_number=None, trustee_number=None,user_email=None, trustee_email=None):
        if process == 1:
            return signup(user_name, password, first_name, last_name, user_number, trustee_number,user_email,trustee_email)
        elif process == 2:
            return login(user_name, password)
        
        elif process == 3:
            return check(user_name)
        else:
            raise ValueError("Invalid process")

    return start(proceed, user_name, password, first_name, last_name,user_number, trustee_number,user_email,trustee_email)

# db_login_signup(1, "test", "p",first_name="Test",last_name="Test",learning_rate="2",understanding_rate="4")

# print(db_login_signup(2, "test user", "password"))







from bson import ObjectId



@st.cache_resource
def save_history(_UserDetails:ObjectId,journal):
    from pymongo import MongoClient
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    MONGO_URI = os.getenv('MONGO_URI')

    connect(MONGO_URI)
    
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
        UserDetails = fields.ReferenceField(User,mongo_name="User Details")
        journal = fields.CharField(mongo_name="Journal")

    def save(_UserDetails,journal):
        history_id=history_ID_query(_UserDetails)

        if history_ID_query(_UserDetails)==[]:
            try:
                new_history = History(UserDetails=_UserDetails,journal=journal)
                new_history.save()
                print("Saved")  
                return new_history
            except Exception as e:
                return f"Couldn't save because {e}"
            
        else:
            history_entry = History.objects.raw({'_id': history_id[0]}).update(
    {"$set": {"Journal": journal}},upsert=True)
    

    return save(_UserDetails,journal)



def get_journal_by_history_id(history_id):
    from pymodm import connect
    from pymodm import connect, MongoModel, fields
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    
    connect(MONGO_URI)
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
    
    history_doc = History.objects.raw({'_id': history_id}).first()
    
    if history_doc:
        journal_content = history_doc.journal
        return journal_content
    else:
        return None  # If history_id not found or no journal content














def history_ID_query(user_id:ObjectId)->list:
    """

    This  function is used to get the list history id's of a user
    to know all the notes a user has saved

    """
    history_ids =[]
    from dotenv import load_dotenv
    from pymodm import connect, MongoModel, fields
    import os
    load_dotenv()
    MONGO_URI= os.getenv('MONGO_URI')
    connect(MONGO_URI)
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
        UserDetails = fields.ReferenceField(User,mongo_name="User Details")
        journal = fields.CharField(mongo_name="Journal")


    history_entries = History.objects.raw({'User Details': user_id})

    
    try:
        for entry in history_entries:
            print(entry)
            history_ids.append(entry._id)
    except Exception as e:
            return  f"Error occurred while fetching data :{e}"
    return history_ids
    

    











    


