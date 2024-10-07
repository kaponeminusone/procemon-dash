from typing import List
from fastapi import APIRouter
from app.db.database import conn
from app.models.user import users
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model= List[User])
async def read_users():
    result = conn.execute(users.select()).mappings().all()  # Cambiado aquí
    users_list = [dict(row) for row in result]
    return users_list


@router.post("/")
async def create_user(user: User):
    new_user = {
        "name": user.name,
        "email": user.email,
    }
    
    # Si 'id' no es necesario que sea proporcionado, no lo incluyas
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    
    # Obtenemos el último usuario insertado utilizando el método 'mappings()'
    user_id = result.inserted_primary_key[0]  # Obtiene el ID del nuevo registro
    return dict(conn.execute(users.select().where(users.c.id == user_id)).mappings().first())
