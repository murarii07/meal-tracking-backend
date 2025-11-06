from fastapi import APIRouter,HTTPException,Header
from models.Model import User,UserCreation
from config.db import Database
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
import bcrypt
from config.db import USER_COLLECTION

auth=APIRouter(prefix="/auth",tags=["Auth"])

def encrypt_str(word:str):
    encode_word=word.encode("utf-8")
    salt=bcrypt.gensalt()
    hash_psw=bcrypt.hashpw(encode_word,salt=salt)
    return hash_psw

   
#user creation
@auth.post("/register",status_code=201)
def register_user(user:UserCreation):
    collection=Database.get_collection(USER_COLLECTION)
    is_exist=collection.find_one({"username":user.username})
    print(is_exist)
    if is_exist:
     raise HTTPException(
        status_code=400,
        detail="user exist please login to different username")
    user.password=encrypt_str(user.password)
    data=collection.insert_one(dict(user))
    return {"message":"user created successfully","user":user.username}



@auth.post("/login")
def login(user:User):
   collection=Database.get_collection(USER_COLLECTION)
   user_doc=collection.find_one({"username":user.username})
   print(user_doc)
   if not user:
    raise HTTPException(
        status_code=400,
        detail="user  does not exist")
   
    is_correct=bcrypt.checkpw(user.password.encode("utf-8"),user_doc.password)
    if not is_correct:
         raise HTTPException(
        status_code=400,
        detail=" user or password mis match try again") 
    
    return {"message":"user created successfully","user":user,"token":"provide token here"}
       
    
   
    

   
   
