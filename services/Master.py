from sqlalchemy.orm import Session
from models.master_data import SKUModel
from schemas.user import ExportRequest, AddSKURequest, UpdateSKURequest
from fastapi import HTTPException
from sqlalchemy import select

def export(db: Session, data: ExportRequest):
    try:
        query = select(SKUModel)
        
        if data.filter_by:
            query = query.where(SKUModel.name.ilike(f"%{data.filter_by}%"))

        results = db.exec(query).all()

        if not results:
            raise HTTPException(404, "No SKU data found.")

        return [row.__dict__ for row in results if '_sa_instance_state' not in row.__dict__]
    
    except Exception as err:
        print("Error.......... export function!\n", err)
        raise HTTPException(500, "Failed to export SKU data.")
    
    #------Add SKU------------->
def add_sku(db: Session, data: AddSKURequest):
    try:
        new_sku = SKUModel(
            name=data.name,
            price=data.price,
            description=data.description
        )

        db.add(new_sku)
        db.commit()
        db.refresh(new_sku)

        return new_sku.__dict__
    
    except Exception as err:
        print("Error.......... add_sku function!\n", err)
        raise HTTPException(500, "Failed to add SKU.")

#------update SKU------------->

def update_sku(db: Session, sku_id: str, data: UpdateSKURequest):
    try:
        sku = db.get(SKUModel, sku_id)

        if not sku:
            raise HTTPException(404, "SKU not found.")

        if data.name is not None:
            sku.name = data.name
        if data.price is not None:
            sku.price = data.price
        if data.description is not None:
            sku.description = data.description

        db.commit()
        db.refresh(sku)

        return sku.__dict__

    except Exception as err:
        print("Error.......... update_sku function!\n", err)
        raise HTTPException(500, "Failed to update SKU.")
    
    #----------Delete SKU----------->

def delete_sku(db: Session, sku_id: str):
    try:
        sku = db.get(SKUModel, sku_id)

        if not sku:
            raise HTTPException(404, "SKU not found.")

        db.delete(sku)
        db.commit()

        return {"message": f"SKU with ID {sku_id} deleted."}

    except Exception as err:
        print("Error.......... delete_sku function!\n", err)
        raise HTTPException(500, "Failed to delete SKU.")

    
    


