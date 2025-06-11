from pydantic import EmailStr
from sqlmodel import Field,SQLModel
from sqlalchemy import Column, Integer, String, Float
from database import Base
from schemas.user import UserRoles

class SKUModel(Base):
    __tablename__ = 'sku_master'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)