from fastapi import HTTPException


class UserError(HTTPException):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserError):
    def __init__(self,user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found" 
        super().__init__(status_code=404,detail=message)

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=401, detail= "Password is incorrect!")

class AuthenticationError(UserError):
    def __init__(self,message : str = "Invalid credentials....."):
        super().__init__(status_code=401,detail=message)
