from pydantic import BaseModel
from typing import Any

class StandardResponse(BaseModel):
    success : bool
    responseCode : str
    responseMessage : str
    data : Any = None
    error : Any = None