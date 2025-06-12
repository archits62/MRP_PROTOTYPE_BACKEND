from enum import Enum
from pydantic import BaseModel,EmailStr,Field

class UserRoles(str, Enum):
    Admin = "Admin"
    User = "User"


class User(BaseModel):
    username : str
    email : EmailStr
    role : UserRoles = UserRoles.User


class UserPrivate(User):
    id : int
    hashed_password : str

class UserPublic(User):
    id : int


class SignupRequest(User):
    password : str
    address : str | None = None


class LoginRequest(BaseModel):
    username : str
    password : str
