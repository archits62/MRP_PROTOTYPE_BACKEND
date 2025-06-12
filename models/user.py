from sqlmodel import SQLModel,Field
from pydantic import EmailStr

from schemas.user import UserRoles


class User(SQLModel,table=True):
    __tablename__ = "users"
    
    id : int | None = Field(default=None,primary_key=True)
    username : str
    email : EmailStr
    role : UserRoles = UserRoles.User
    hashed_password : str