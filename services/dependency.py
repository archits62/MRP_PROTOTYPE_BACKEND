from typing import Annotated
from sqlmodel import Session
from fastapi import Depends

from database.db_connection import get_session



# """Create a session of DB connection"""
sessionDep = Annotated[Session,Depends(get_session)]