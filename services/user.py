from fastapi import HTTPException
from sqlmodel import select
from argon2 import PasswordHasher
import jwt

from config import Config
from services.dependency import sessionDep
from schemas.user import SignupRequest,LoginRequest,UserPublic,TokenPayload
from models.user import User as UserModel
from utils.custom_exceptions import AuthenticationError


ph = PasswordHasher()

def get_hashed_password(plain_password:str):
    return ph.hash(plain_password)


def verify_password(hashed_Password : str ,plain_password : str):
    try:
        return ph.verify(hashed_Password, plain_password)
    except Exception as err:
        print("There is error while verify password , verfiy_password function......!", err)
        return False
    
  
def create_access_token( user : UserModel ):
    token = TokenPayload(
        id=user.id,
        username=user.username,
        role=user.role
    )

    return jwt.encode(token.model_dump(),Config.JWT_SECRET_KEY,Config.ALGORITHM)

def verify_access_token(token : str ):
    try:
        token = jwt.decode(token,Config.JWT_SECRET_KEY,Config.ALGORITHM)
        return token
    except Exception as e:
        print("Error....! invalid token")
        return None


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
        is_user_authentic = verify_password(user.hashed_password,data.password)

        if not is_user_authentic:
            raise AuthenticationError("Invalid password...")


        # create a jwt token
        access_token = create_access_token(user)

        return {
            "access_token" : access_token,
            "user" : UserPublic(**user.model_dump())
        }

    except HTTPException as http_err:
        raise http_err
    
    except Exception as err :
        print("Error........... login function!\n",err)
        raise HTTPException(500,"User login failed!")