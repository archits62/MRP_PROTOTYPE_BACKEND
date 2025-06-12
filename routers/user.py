from fastapi import APIRouter

from services.dependency import sessionDep
from schemas.user import SignupRequest,LoginRequest
import services.user as UserService
from utils.response_handler import success_response

router = APIRouter()


@router.post("/signup")
def signup_user( db : sessionDep,singup_data : SignupRequest):
    new_user = UserService.register(db, singup_data)
    return success_response("User register successfully!",new_user)


@router.post("/login")
def login_user( db : sessionDep, login_data : LoginRequest):
    user_and_token = UserService.login(db,login_data)
    return success_response("Logged In user", user_and_token)