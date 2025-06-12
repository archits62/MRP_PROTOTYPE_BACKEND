from argon2 import PasswordHasher
import jwt

from config import Config
from schemas.user import TokenPayload
from models.user import User as UserModel


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

def decode_access_token(token : str ):
    try:
        payload = jwt.decode(token,Config.JWT_SECRET_KEY,Config.ALGORITHM)
        return payload
    except Exception as e:
        print("Error....! invalid token")
        return None
