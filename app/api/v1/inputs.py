
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.db.database import conn
from app.models.models import Entradas
from app.schemas.input import Input, InputRead, InputUpdate
from typing import List

router = APIRouter()

inputs = Entradas.__table__

@router.get("/", response_model=List[InputRead])
async def read_inputs():
    # Ejecuta la consulta y obtén los resultados como un iterable de diccionarios
    result = conn.execute(inputs.select()).mappings()
    # Utiliza model_validate para validar y crear una lista de InputRead
    inputs_list = [InputRead.model_validate(row) for row in result]

    return inputs_list

@router.get("/search/", response_model=List[InputRead])
async def search_inputs(name: str = None, id: int = None):
    # Crear la consulta base
    query = select(inputs)
    # Filtrar por nombre y id, si se proporciona
    if name:
        query = query.where(inputs.c.nombre.ilike(f'%{name}%'))  # Búsqueda sin importar mayúsculas
    if id is not None:
        query = query.where(inputs.c.id == id)  # Búsqueda por id
    # Ejecutar la consulta y obtener el resultado
    result = conn.execute(query).mappings()
    # Validar el resultado y devolverlo
    if result:
        inputs_list = [InputRead.model_validate(row) for row in result]
        return inputs_list
    else:
        raise HTTPException(status_code=404, detail="Input not found")
    

@router.post("/", response_model=InputRead)
async def create_input(input: Input):
    # Crea un nuevo diccionario para el usuario
    # new_input = {
    #     "id": input.id,
    #     "nombre": input.name,  # Asegúrate de que el nombre de la columna sea correcto
    #     "tipo": input.type
    # }

    new_input = input.model_dump(exclude_unset=True, by_alias=True)
    
    result = conn.execute(inputs.insert().values(new_input))
    conn.commit()
    
    input_id = result.inserted_primary_key[0]
    created_input = conn.execute(inputs.select().where(inputs.c.id == input_id)).mappings().first()
    return InputRead.model_validate(created_input)

@router.put("/", response_model=InputRead)
async def update_input(input: InputUpdate):

    existing_input = conn.execute(inputs.select().where(inputs.c.id == input.id)).mappings().first()
    if not existing_input:
        raise HTTPException(status_code=404, detail="Input not found")
    
    update_data = input.model_dump(exclude_unset=True, by_alias=True)

    conn.execute(
        inputs.update().where(inputs.c.id == input.id)
        .values(update_data)
        )
    conn.commit()
    
    updated_input = conn.execute(inputs.select().where(inputs.c.id == input.id)).mappings().first()

    return InputRead.model_validate(updated_input)

