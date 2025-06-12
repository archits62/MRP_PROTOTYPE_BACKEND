from fastapi import HTTPException
from sqlmodel import select

from services.dependency import sessionDep
from schemas.user import SignupRequest,UserPublic
from models.user import User as UserModel


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

        # store user into db
        new_user = UserModel(
            username=data.username,
            email=data.email,
            role=data.role,
            hashed_password=data.password
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