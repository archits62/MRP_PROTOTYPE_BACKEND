from fastapi import APIRouter, Depends

from services.dependency import sessionDep,get_admin_user
from schemas.cabinet import CabinetCreate, CabinetUpdate
import services.cabinet as CabinetService
from utils.response_handler import success_response

router = APIRouter()



# // ********************** Get All Cabinets ***************************
@router.get("/")
def get_all_cabinets(db: sessionDep, skip: int = 0, limit: int = 100):
    cabinets = CabinetService.get_all_cabinets(db, skip=skip, limit=limit)
    return success_response("Cabinets fetched successfully!", cabinets)



# // ********************** Get Cabinet by ID ***************************
@router.get("/{id}")
def get_cabinet_by_id(db: sessionDep, id: int):
    cabinet = CabinetService.get_cabinet_by_id(db, id)
    return success_response("Cabinet fetched successfully!", cabinet)



# // ------------------------------------------ Protected Routes -----------------------------------------



# // ********************** Create Cabinet ***************************
@router.post("/")
def create_cabinet(db: sessionDep, cabinet_data: CabinetCreate, _=Depends(get_admin_user)):
    new_cabinet = CabinetService.create_cabinet(db, cabinet_data)
    return success_response("Cabinet created successfully!", new_cabinet)



# // ********************** Create Cabinets Bulk ***************************
@router.post("/bulk")
def create_cabinets_bulk(db: sessionDep, bulk_data: list[CabinetCreate], _=Depends(get_admin_user)):
    new_cabinets = CabinetService.create_cabinets_bulk(db, bulk_data)
    return success_response(f"{len(new_cabinets)} cabinets created successfully!", new_cabinets)



# // ********************** Update Cabinet ***************************
@router.put("/{id}")
def update_cabinet(db: sessionDep, id: int, cabinet_data: CabinetUpdate, _=Depends(get_admin_user)):
    updated_cabinet = CabinetService.update_cabinet(db, id, cabinet_data)
    return success_response("Cabinet updated successfully!", updated_cabinet)



# // ********************** Delete Cabinet ***************************
@router.delete("/{id}")
def delete_cabinet(db: sessionDep, id: int, _=Depends(get_admin_user)):
    CabinetService.delete_cabinet(db, id)
    return success_response("Cabinet deleted successfully!", None) 