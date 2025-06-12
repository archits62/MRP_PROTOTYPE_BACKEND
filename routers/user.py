from fastapi import APIRouter

from services.dependency import sessionDep
from schemas.user import SignupRequest
import services.user as UserService
from utils.response_handler import success_response

router = APIRouter()


@router.post("/signup")
def signup_user( db : sessionDep,singup_data : SignupRequest):
    new_user = UserService.register(db, singup_data)
    return success_response("User register successfully!",new_user)