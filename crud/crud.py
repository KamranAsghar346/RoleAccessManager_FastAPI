from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CRUDUser:
    def get_by_username(self, db: Session, username: str):
        return db.query(models.User).filter(models.User.username == username).first()

    def create(self, db: Session, user: schemas.UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = models.User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate(self, db: Session, username: str, password: str):
        user = self.get_by_username(db, username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

class CRUDInventory:
    def create(self, db: Session, inventory: schemas.InventoryCreate, created_by: int):
        db_inventory = models.Inventory(**inventory.dict(), created_by=created_by)
        db.add(db_inventory)
        db.commit()
        db.refresh(db_inventory)
        return db_inventory

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Inventory).offset(skip).limit(limit).all()

    def update(self, db: Session, inventory_id: int, inventory: schemas.InventoryCreate):
        db_inventory = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
        if db_inventory:
            for key, value in inventory.dict().items():
                setattr(db_inventory, key, value)
            db.commit()
            db.refresh(db_inventory)
        return db_inventory

    def delete(self, db: Session, inventory_id: int):
        db_inventory = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
        if db_inventory:
            db.delete(db_inventory)
            db.commit()
            return True
        return False

user_crud = CRUDUser()
inventory_crud = CRUDInventory()