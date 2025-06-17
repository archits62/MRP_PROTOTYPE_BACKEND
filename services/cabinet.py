from fastapi import HTTPException
from sqlmodel import select

from services.dependency import sessionDep
from schemas.cabinet import CabinetCreate, CabinetRead, CabinetUpdate
from models.cabinet import Cabinet as CabinetModel


def get_cabinet_by_cabinet_id(db: sessionDep, cabinet_id: str):
    try:
        query = select(CabinetModel).where(CabinetModel.cabinet_id == cabinet_id)
        return db.exec(query).first()
    except Exception as e:
        return None


def create_cabinet(db: sessionDep, data: CabinetCreate) -> CabinetRead:
    try:
        # Check if cabinet_id already exists
        existing_cabinet = get_cabinet_by_cabinet_id(db, data.cabinet_id)
        if existing_cabinet:
            raise HTTPException(400, "Cabinet ID already exists")

        new_cabinet = CabinetModel(**data.model_dump())

        db.add(new_cabinet)
        db.commit()
        db.refresh(new_cabinet)

        return CabinetRead(**new_cabinet.model_dump())
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        db.rollback()
        print("create_cabinet function error:", e)
        raise HTTPException(500, "Internal server error")


def create_cabinets_bulk(db: sessionDep, cabinets_data: list[CabinetCreate]) -> list[CabinetRead]:
    try:
        # Check for duplicate cabinet_ids in the input data
        cabinet_ids = [cabinet.cabinet_id for cabinet in cabinets_data]
        if len(cabinet_ids) != len(set(cabinet_ids)):
            raise HTTPException(400, "Duplicate cabinet IDs found in input data")

        # Check if any cabinet_id already exists in database
        for cabinet_data in cabinets_data:
            existing_cabinet = get_cabinet_by_cabinet_id(db, cabinet_data.cabinet_id)
            if existing_cabinet:
                raise HTTPException(400, f"Cabinet ID '{cabinet_data.cabinet_id}' already exists")

        # Create all cabinets
        new_cabinets = []
        for cabinet_data in cabinets_data:
            new_cabinet = CabinetModel(**cabinet_data.model_dump())
            new_cabinets.append(new_cabinet)
            db.add(new_cabinet)

        db.commit()
        
        # Refresh all cabinets to get their IDs
        for cabinet in new_cabinets:
            db.refresh(cabinet)

        return [CabinetRead(**cabinet.model_dump()) for cabinet in new_cabinets]
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        db.rollback()
        print("create_cabinets_bulk function error:", e)
        raise HTTPException(500, "Internal server error")


def get_all_cabinets(db: sessionDep, skip: int = 0, limit: int = 100) -> list[CabinetRead]:
    try:
        query = select(CabinetModel).offset(skip).limit(limit)
        cabinets = db.exec(query).all()
        return [CabinetRead(**cabinet.model_dump()) for cabinet in cabinets]
    
    except Exception as e:
        print("get_all_cabinets function error:", e)
        raise HTTPException(500, "Failed to fetch cabinets")


def get_cabinet_by_id(db: sessionDep, id: int) -> CabinetRead:
    try:
        query = select(CabinetModel).where(CabinetModel.id == id)
        cabinet = db.exec(query).first()
        
        if not cabinet:
            raise HTTPException(status_code=404, detail="Cabinet not found")
            
        return CabinetRead(**cabinet.model_dump())
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        print("get_cabinet_by_id function error:", e)
        raise HTTPException(500, "Failed to fetch cabinet")


def update_cabinet(db: sessionDep, cabinet_id: int, data: CabinetUpdate) -> CabinetRead:
    try:
        query = select(CabinetModel).where(CabinetModel.id == cabinet_id)
        cabinet = db.exec(query).first()
        
        if not cabinet:
            raise HTTPException(status_code=404, detail="Cabinet not found")
        
        # Check if cabinet_id is being updated and if it already exists
        if data.cabinet_id and data.cabinet_id != cabinet.cabinet_id:
            existing_cabinet = get_cabinet_by_cabinet_id(db, data.cabinet_id)
            if existing_cabinet:
                raise HTTPException(400, "Cabinet ID already exists")
        
        # Update only provided fields
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cabinet, field, value)
        
        db.add(cabinet)
        db.commit()
        db.refresh(cabinet)
        
        return CabinetRead(**cabinet.model_dump())

    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        db.rollback()
        print("update_cabinet function error:", e)
        raise HTTPException(500, "Failed to update cabinet")


def delete_cabinet(db: sessionDep, cabinet_id: int) -> bool:
    try:
        query = select(CabinetModel).where(CabinetModel.id == cabinet_id)
        cabinet = db.exec(query).first()
        
        if not cabinet:
            raise HTTPException(status_code=404, detail="Cabinet not found")
        
        db.delete(cabinet)
        db.commit()
        
        return True
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        db.rollback()
        print("delete_cabinet function error:", e)
        raise HTTPException(500, "Failed to delete cabinet") 