from typing import Annotated
from sqlmodel import Session
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from database.db_connection import get_session
#from .auth import decode_token
from utils.exceptions import AuthenticationError,UserNotFoundError
from models.user import User as UserModel
from schemas.user import UserRoles



# """Create a session of DB connection"""
sessionDep = Annotated[Session,Depends(get_session)]