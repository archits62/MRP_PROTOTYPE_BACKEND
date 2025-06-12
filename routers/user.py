from fastapi import APIRouter,Depends

from services.dependency import sessionDep
from schemas.user import SignupRequest,LoginRequest
import services.user as UserService
from services.dependency import get_admin_user
from utils.response_handler import success_response

router = APIRouter()



# // ********************** Singup User ***************************
@router.post("/signup")
def signup_user( db : sessionDep,singup_data : SignupRequest):
    new_user = UserService.register(db, singup_data)
    return success_response("User register successfully!",new_user)



# // ********************** Login User ***************************
@router.post("/login")
def login_user( db : sessionDep, login_data : LoginRequest):
    user_and_token = UserService.login(db,login_data)
    return success_response("Logged In user", user_and_token)



# # ----------------------------------- Admin Routes -------------------------------

# // ********************** Get User- List ***************************
@router.get("/getuserlist")
def get_users_list(db : sessionDep, _ = Depends(get_admin_user)):
    users =  UserService.get_user_list(db)
    return success_response("Users list fetched successfully!",users)

# ---------------------------------------------------------------------------------
