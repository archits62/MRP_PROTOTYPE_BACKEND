from typing import Annotated
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session,select

from database.db_connection import get_session
from models.user import User as UserModel
from schemas.user import UserRoles
import services.auth as AuthService
from utils.custom_exceptions import AuthenticationError,UserNotFoundError


# """Create a session of DB connection"""
sessionDep = Annotated[Session,Depends(get_session)]


# """Check is token include or not in request"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def get_current_user(db:sessionDep, token : Annotated[str, Depends( oauth2_scheme )]):
    try:
        payload = AuthService.decode_access_token(token)

        if not payload :
            raise AuthenticationError()
        
        user_id = payload.get("id")

        user = db.exec(select(UserModel).where(UserModel.id == user_id)).first()

        print( user , "user in get current user")


        if not user:
            raise UserNotFoundError(user_id)

        return user
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as err :
        print("Error........... get current user function\n!",err)
        raise HTTPException(500,"Failed to get current user!")
    
    

def get_admin_user(user : Annotated[UserModel,Depends(get_current_user)]):
    if user.role != UserRoles.Admin:
        raise AuthenticationError("User is not authorized as 'admin' user!")
    return user