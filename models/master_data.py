from pydantic import EmailStr
from sqlmodel import Field,SQLModel


class SKUModel(SQLModel,table=True):
    __tablename__ = 'sku_master'

    id : int | None = Field(default=None, primary_key=True)
    name : str
    price : int
    description : str | None = None