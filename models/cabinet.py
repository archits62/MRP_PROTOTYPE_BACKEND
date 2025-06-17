from sqlmodel import SQLModel, Field,func,Column,DateTime
from datetime import datetime,timezone

class Cabinet(SQLModel,table=True):
    __tablename__ = "cabinets"

    id : int | None = Field(default=None,primary_key= True)
    cabinet_id : str = Field(unique=True,description="Cabinet ID")
    product_line : str
    product_category : str
    product_family : str
    product_model : str
    width : int = Field(gt=0,description="Width in mm")
    height : int = Field(gt=0,description="Height in mm")
    depth : int = Field(gt=0, description="Depth in mm")
    material : str
    finish : str
    hardware : str
    configuration : str
    product_description : str

    created_at : datetime = Field(default_factory= lambda : datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory= lambda : datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), onupdate=func.now()))
