from fastapi import APIRouter, HTTPException, Depends
from app.db.database import get_db  # Importa la función desde db.py
from sqlalchemy.orm import Session
from app.models.models import Usuario
from app.schemas.user import User, UserRead, UserUpdate
from typing import List

router = APIRouter()

users = Usuario.__table__

@router.get("/", response_model=List[UserRead])
async def read_users(db: Session = Depends(get_db)):
    result = db.execute(users.select()).mappings()
    users_list = [UserRead.model_validate(row) for row in result]
    return users_list

@router.get("/{email}", response_model=UserRead)
async def read_user(email: str, db: Session = Depends(get_db)):
    result = db.execute(users.select().where(users.c.email == email)).mappings().first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = UserRead.model_validate(result)
    return user

@router.post("/", response_model=UserRead)
async def create_user(user: User, db: Session = Depends(get_db)):
    new_user = {
        "id": user.id,
        "nombre": user.username,
        "email": user.email,
        "tipo": user.role
    }

    result = db.execute(users.insert().values(new_user))
    db.commit()
    
    user_id = result.inserted_primary_key[0]
    created_user = db.execute(users.select().where(users.c.id == user_id)).mappings().first()
    
    return UserRead.model_validate(created_user)

@router.put("/", response_model=UserRead)
async def update_user(user: UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.execute(users.select().where(users.c.id == user.id)).mappings().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True, by_alias=True)
    db.execute(users.update().where(users.c.id == user.id).values(update_data))
    db.commit()
    
    updated_user = db.execute(users.select().where(users.c.id == user.id)).mappings().first()

    return UserRead.model_validate(updated_user)
