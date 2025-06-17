from pydantic import BaseModel
from datetime import datetime

class CabinetCreate(BaseModel):
    sku_code: str
    product_line: str
    product_category: str
    product_family: str
    product_model: str
    width: int
    height: int
    depth: int
    material: str
    finish: str
    hardware: str
    configuration: str
    product_description: str

class CabinetRead(BaseModel):
    id : int
    sku_code: str
    product_line: str
    product_category: str
    product_family: str
    product_model: str
    width: int
    height: int
    depth: int
    material: str
    finish: str
    hardware: str
    configuration: str
    product_description: str
    created_at: datetime
    updated_at: datetime

class CabinetUpdate(BaseModel):
    # id : int # will come form url path ??
    sku_code: str | None
    product_line: str | None
    product_category: str | None
    product_family: str | None
    product_model: str | None
    width: int | None
    height: int | None
    depth: int | None
    material: str | None
    finish: str | None
    hardware: str | None
    configuration: str | None
    product_description: str | None