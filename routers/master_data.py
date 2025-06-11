from fastapi import APIRouter

from utils.response_handler import success_response
import services.Master as Master_service
from services.dependency import sessionDep
from schemas.user import ExportRequest
from schemas.user import AddSKURequest
from schemas.user import UpdateSKURequest


router = APIRouter()

@router.post("/sku/export")
async def export(db: sessionDep, data: ExportRequest):
    rows = Master_service.export(db, data)


@router.post("/sku")
async def add_sku_data( db: sessionDep, data: AddSKURequest,):
    new_data = Master_service.add_sku(db, data)
    return success_response("SKU added", new_data)

@router.put("/sku/{sku_id}")
async def update_sku_data( db: sessionDep, sku_id: str, data: UpdateSKURequest,):
    updated_data = Master_service.update_sku(db, sku_id, data)
    return success_response("SKU updated", updated_data)

@router.delete("/sku/{sku_id}")
async def delete_sku_data( db: sessionDep, sku_id: str,):
    deleted_data = Master_service.delete_sku(db, sku_id)
    return success_response("SKU deleted", deleted_data)