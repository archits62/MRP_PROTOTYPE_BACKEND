from fastapi import HTTPException
from sqlmodel import select

from services.dependency import sessionDep
from schemas.user import SignupRequest,LoginRequest,UserPublic
from models.user import User as UserModel
from utils.custom_exceptions import AuthenticationError
import services.auth as AuthService


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


        hashed_password = AuthService.get_hashed_password(data.password)

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
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        db.rollback()
        print("register function.............! \n",e)
        raise HTTPException(500,"Internal server Error...!\n")
    

def login( db : sessionDep , data : LoginRequest):
    try:

        # is user exits
        user = get_user_by_username(db,data.username)

        if not user:
            raise AuthenticationError("User is not found!")
        
        # verify password
        is_user_authentic = AuthService.verify_password(user.hashed_password,data.password)

        if not is_user_authentic:
            raise AuthenticationError("Invalid password...")


        # create a jwt token
        access_token = AuthService.create_access_token(user)

        return {
            "access_token" : access_token,
            "user" : UserPublic(**user.model_dump())
        }

    except HTTPException as http_err:
        raise http_err
    
    except Exception as err :
        print("Error........... login function!\n",err)
        raise HTTPException(500,"User login failed!")
    

def get_user_list( db : sessionDep ) -> list[UserPublic]:
    try:
        users = db.exec(select(UserModel)).all()
        return [ UserPublic(**user.model_dump()) for user in users]

    except Exception as err :
        print("Error........... get_user_list function!\n",err)
        raise HTTPException(500,"Failed to fetched get_user_list!")