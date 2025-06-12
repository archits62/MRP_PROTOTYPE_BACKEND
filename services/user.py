from fastapi import HTTPException
from sqlmodel import select
from argon2 import PasswordHasher

from services.dependency import sessionDep
from schemas.user import SignupRequest,UserPublic
from models.user import User as UserModel


ph = PasswordHasher()

def get_hashed_password(plain_password:str):
    return ph.hash(plain_password)
  

def get_user_by_username(db:sessionDep,username : str):
    try:
        query = select(UserModel).where( UserModel.username == username )
        return db.exec(query).first()
    except Exception as e:
        return None



def register(db : sessionDep , data : SignupRequest) -> UserPublic:
    try:
        # check is user already register by username
        user = get_user_by_username(db, data.username)
        
        if user:
            raise HTTPException(400,"User already registerd with this name.")


        hashed_password = get_hashed_password(data.password)

        # store user into db
        new_user = UserModel(
            username=data.username,
            email=data.email,
            role=data.role,
            hashed_password=hashed_password
        )


        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserPublic(**new_user.model_dump())
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        db.rollback()
        print("register function.............! \n",e)
        raise HTTPException(500,"Internal server Error...!\n")