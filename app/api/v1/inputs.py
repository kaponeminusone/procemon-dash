from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_db  # Importa la función desde db.py
from app.models.models import Entradas
from app.schemas.input import Input, InputRead, InputUpdate
from typing import List

router = APIRouter()

inputs = Entradas.__table__

@router.get("/", response_model=List[InputRead])
async def read_inputs(db: Session = Depends(get_db)):
    # Ejecuta la consulta y obtén los resultados como un iterable de diccionarios
    result = db.execute(inputs.select()).mappings()
    # Utiliza model_validate para validar y crear una lista de InputRead
    inputs_list = [InputRead.model_validate(row) for row in result]
    return inputs_list

@router.get("/search/", response_model=List[InputRead])
async def search_inputs(name: str = None, id: int = None, db: Session = Depends(get_db)):
    # Crear la consulta base
    query = select(inputs)
    # Filtrar por nombre y id, si se proporciona
    if name:
        query = query.where(inputs.c.nombre.ilike(f'%{name}%'))  # Búsqueda sin importar mayúsculas
    if id is not None:
        query = query.where(inputs.c.id == id)  # Búsqueda por id
    # Ejecutar la consulta y obtener el resultado
    result = db.execute(query).mappings()
    # Validar el resultado y devolverlo
    inputs_list = [InputRead.model_validate(row) for row in result]
    if inputs_list:
        return inputs_list
    else:
        raise HTTPException(status_code=404, detail="Input not found")

@router.post("/", response_model=InputRead)
async def create_input(input: Input, db: Session = Depends(get_db)):
    new_input = input.model_dump(exclude_unset=True, by_alias=True)
    
    result = db.execute(inputs.insert().values(new_input))
    db.commit()
    
    input_id = result.inserted_primary_key[0]
    created_input = db.execute(inputs.select().where(inputs.c.id == input_id)).mappings().first()
    return InputRead.model_validate(created_input)

@router.put("/", response_model=InputRead)
async def update_input(input: InputUpdate, db: Session = Depends(get_db)):
    existing_input = db.execute(inputs.select().where(inputs.c.id == input.id)).mappings().first()
    if not existing_input:
        raise HTTPException(status_code=404, detail="Input not found")
    
    update_data = input.model_dump(exclude_unset=True, by_alias=True)

    db.execute(
        inputs.update().where(inputs.c.id == input.id)
        .values(update_data)
    )
    db.commit()
    
    updated_input = db.execute(inputs.select().where(inputs.c.id == input.id)).mappings().first()

    return InputRead.model_validate(updated_input)
