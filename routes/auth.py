import uuid

import bcrypt
import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth_middleware import auth_middleware
from models.user import User
from pydantic_schema.user_create import UserCreate
from pydantic_schema.user_login import UserLogin

router =APIRouter()
 
# Signup route
@router.post('/signup', status_code=201)
def signup_user(user: UserCreate,db: Session = Depends(get_db)):
    # Check if user already exists
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(status_code=400, detail='User already exists!')

    # Hash the password
    hash_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    
    # Create a new user object
    user_db = User(id=str(uuid.uuid4()), email=user.email, password=hash_pw, name=user.name)

    # Add the user to the database
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    
    # Return a serializable response (e.g., converting user_db to a dictionary)
    return {"id": user_db.id, "name": user_db.name, "email": user_db.email}


@router.post('/login', status_code=201)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    #if user with same email already exists
    user_db=db.query(User).filter(User.email==user.email).first()

    if not user_db:
        raise HTTPException(400,'User doesnt exist')
    
    #password matching
    try:
        is_match = bcrypt.checkpw(user.password.encode(), user_db.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Password verification failed: {str(e)}")
    
    if not is_match:
        raise HTTPException(400,'Password Didnt Match')
    

    token=jwt.encode({'id': user_db.id},'password_key')

    return {'token':token, 'user':user_db}


@router.get('/')
def curr_user_data(db: Session=Depends(get_db),user_dict =Depends(auth_middleware)):
    user=db.query(User).filter(User.id==user_dict['uid']).first()

    if not user:
        raise HTTPException(404,'User Not Found')
    
    return user

    