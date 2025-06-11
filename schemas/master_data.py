from pydantic import BaseModel
from typing import Optional

class ExportRequest(BaseModel):
    filter_by: Optional[str] = None  # Adjust fields as per your actual filtering logic

class   AddSKURequest(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class UpdateSKURequest(BaseModel):
    name: Optional[str]
    price: Optional[float]
    description: Optional[str] = None

class SignupRequest(BaseModel):  # This was missing BaseModel
    password: str
    verifyPassword: str
    address: Optional[str] = None