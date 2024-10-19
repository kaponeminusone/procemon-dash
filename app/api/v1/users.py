
from fastapi import APIRouter, HTTPException
from app.db.database import conn
from app.models.models import Usuario
from app.schemas.user import User, UserRead, UserUpdate
from typing import List

router = APIRouter()

users = Usuario.__table__

@router.get("/", response_model=List[UserRead])
async def read_users():
    # Ejecuta la consulta y obtén los resultados como un iterable de diccionarios
    result = conn.execute(users.select()).mappings()
    # Utiliza model_validate para validar y crear una lista de UserRead
    users_list = [UserRead.model_validate(row) for row in result]

    return users_list

@router.get("/{email}", response_model=UserRead)
async def read_users(email: str):
    # Ejecuta la consulta y obtén los resultados como un iterable de diccionarios
    result = conn.execute(users.select().where(users.c.email == email)).mappings().first()
    # Utiliza model_validate para validar y crear una lista de UserRead
    user = UserRead.model_validate(result)

    return user

@router.post("/", response_model=UserRead)
async def create_user(user: User): #TODO: Validacion para error en la inserción
    # Crea un nuevo diccionario para el usuario
    new_user = {
        "id": user.id,
        "nombre": user.username,  # Asegúrate de que el nombre de la columna sea correcto
        "email": user.email,
        "tipo": user.role
    }
    
    # Inserta el nuevo usuario en la base de datos
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    
    # Obtiene el último usuario insertado utilizando mappings
    user_id = result.inserted_primary_key[0]
    created_user = conn.execute(users.select().where(users.c.id == user_id)).mappings().first()
    
    # Valida y retorna el usuario creado como UserRead
    return UserRead.model_validate(created_user)

@router.put("/", response_model=UserRead)
async def update_user(user: UserUpdate):

    existing_user = conn.execute(users.select().where(users.c.id == user.id)).mappings().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True, by_alias=True)

    conn.execute(
        users.update().where(users.c.id == user.id)
        .values(update_data)
        )
    conn.commit()
    
    updated_user = conn.execute(users.select().where(users.c.id == user.id)).mappings().first()

    return UserRead.model_validate(updated_user)


# from fastapi import APIRouter
# from app.db.database import conn
# from app.models.models import users
# from app.schemas.user import User
# from typing import List

# router = APIRouter()

# @router.get("/", response_model= List[User])
# async def read_users():
#     result = conn.execute(users.select()).mappings().all()  # Cambiado aquí
#     users_list = [dict(row) for row in result]
#     return users_list


# @router.post("/")
# async def create_user(user: User):
#     new_user = {
#         "name": user.name,
#         "email": user.email,
#     }
    
#     # Si 'id' no es necesario que sea proporcionado, no lo incluyas
#     result = conn.execute(users.insert().values(new_user))
#     conn.commit()
    
#     # Obtenemos el último usuario insertado utilizando el método 'mappings()'
#     user_id = result.inserted_primary_key[0]  # Obtiene el ID del nuevo registro
#     return dict(conn.execute(users.select().where(users.c.id == user_id)).mappings().first())
