from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_db  # Importa la función desde db.py
from app.models.models import Indicadores
from app.schemas.indicator import Indicator, IndicatorRead, IndicatorUpdate
from typing import List

router = APIRouter()

indicators = Indicadores.__table__

@router.get("/", response_model=List[IndicatorRead])
async def read_indicators(db: Session = Depends(get_db)):
    # Ejecuta la consulta y obtén los resultados como un iterable de diccionarios
    result = db.execute(indicators.select()).mappings()
    # Utiliza model_validate para validar y crear una lista de IndicatorRead
    indicators_list = [IndicatorRead.model_validate(row) for row in result]
    return indicators_list

@router.get("/search/", response_model=List[IndicatorRead])
async def search_indicators(name: str = None, id: int = None, db: Session = Depends(get_db)):
    # Crear la consulta base
    query = select(indicators)
    # Filtrar por nombre y id, si se proporciona
    if name:
        query = query.where(indicators.c.nombre.ilike(f'%{name}%'))  # Búsqueda sin importar mayúsculas
    if id is not None:
        query = query.where(indicators.c.id == id)  # Búsqueda por id
    # Ejecutar la consulta y obtener el resultado
    result = db.execute(query).mappings()
    # Validar el resultado y devolverlo
    indicators_list = [IndicatorRead.model_validate(row) for row in result]
    if indicators_list:
        return indicators_list
    else:
        raise HTTPException(status_code=404, detail="Indicator not found")

@router.post("/", response_model=IndicatorRead)
async def create_indicator(input: Indicator, db: Session = Depends(get_db)):
    new_input = input.model_dump(exclude_unset=True, by_alias=True)
    
    result = db.execute(indicators.insert().values(new_input))
    db.commit()
    
    input_id = result.inserted_primary_key[0]
    created_input = db.execute(indicators.select().where(indicators.c.id == input_id)).mappings().first()
    return IndicatorRead.model_validate(created_input)

@router.put("/", response_model=IndicatorRead)
async def update_indicator(input: IndicatorUpdate, db: Session = Depends(get_db)):
    existing_input = db.execute(indicators.select().where(indicators.c.id == input.id)).mappings().first()
    if not existing_input:
        raise HTTPException(status_code=404, detail="Indicator not found")
    
    update_data = input.model_dump(exclude_unset=True, by_alias=True)

    db.execute(
        indicators.update().where(indicators.c.id == input.id)
        .values(update_data)
    )
    db.commit()
    
    updated_input = db.execute(indicators.select().where(indicators.c.id == input.id)).mappings().first()

    return IndicatorRead.model_validate(updated_input)
