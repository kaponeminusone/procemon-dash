# app/api/routes/procesos.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db  # Importa la función desde db.py
from app.models.models import Procesos, Etapas, Entradas, Indicadores, EtapaIndicadores, EtapasEntradas, EtapasSalidas
from app.schemas.proceso import ProcesoCreate, ProcesoResponse  # Asegúrate de que las clases existan en el archivo schemas
from typing import List

router = APIRouter()

procesos_table = Procesos.__table__

@router.post("/", response_model=ProcesoResponse)
async def create_proceso(proceso: ProcesoCreate, db: Session = Depends(get_db)):
    # Crea un nuevo diccionario para el proceso
    new_proceso = {
        "nombre": proceso.nombre,
        "num_etapas": len(proceso.etapas)
    }
    
    # Inserta el nuevo proceso en la base de datos
    result = db.execute(procesos_table.insert().values(new_proceso))
    db.commit()
    
    # Obtiene el último proceso insertado
    proceso_id = result.inserted_primary_key[0]
    
    # Inserta las etapas relacionadas
    for etapa in proceso.etapas:
        new_etapa = {
            "num_etapa": etapa.num_etapa,
            "id_proceso": proceso_id
        }
        etapa_result = db.execute(Etapas.__table__.insert().values(new_etapa))
        db.commit()

        etapa_id = etapa_result.inserted_primary_key[0]

        # Inserta las entradas, indicadores y salidas para cada etapa
        for entrada in etapa.entradas:
            db.execute(EtapasEntradas.__table__.insert().values(id_etapa=etapa_id, id_entrada=entrada.id))
            db.commit()

        for indicador in etapa.indicadores:
            db.execute(EtapaIndicadores.__table__.insert().values(id_etapa=etapa_id, id_indicador_entrada=indicador.id))
            db.commit()

        for salida in etapa.salidas:
            db.execute(EtapasSalidas.__table__.insert().values(id_etapa=etapa_id, id_entrada=salida.id))
            db.commit()
    
    # Obtiene el proceso creado con las etapas y detalles completos
    created_proceso = db.execute(procesos_table.select().where(procesos_table.c.id == proceso_id)).mappings().first()

    return ProcesoResponse.model_validate(created_proceso)
