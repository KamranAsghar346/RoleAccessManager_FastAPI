from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.crud import inventory_crud
from schemas import schemas
from permissions.checker import require_permission
from permissions.roles import Action, Resource
from api.endpoints.auth import get_current_user
from models.models import User

router = APIRouter()

@router.post("/", response_model=schemas.Inventory)
@require_permission(Resource.INVENTORY, Action.CREATE)
async def create_inventory_item(
    inventory: schemas.InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new inventory item (Master and Vendor only)"""
    return inventory_crud.create(db=db, inventory=inventory, created_by=current_user.id)

@router.get("/", response_model=list[schemas.Inventory])
@require_permission(Resource.INVENTORY, Action.READ)
async def read_inventory(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Read inventory (All roles)"""
    return inventory_crud.get_all(db, skip=skip, limit=limit)

@router.put("/{inventory_id}", response_model=schemas.Inventory)
@require_permission(Resource.INVENTORY, Action.UPDATE)
async def update_inventory_item(
    inventory_id: int,
    inventory: schemas.InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update inventory item (Master only)"""
    return inventory_crud.update(db=db, inventory_id=inventory_id, inventory=inventory)

@router.delete("/{inventory_id}")
@require_permission(Resource.INVENTORY, Action.DELETE)
async def delete_inventory_item(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete inventory item (Master only)"""
    success = inventory_crud.delete(db=db, inventory_id=inventory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return {"message": "Inventory item deleted successfully"}