from fastapi import APIRouter, HTTPException
from app.db.database import conn
from app.models.models import Procesos, Etapas, Entradas, Indicadores, EtapaIndicadores, EtapasEntradas, EtapasSalidas
from app.schemas.proceso import ProcesoCreate, ProcesoResponse  # Asegúrate de que las clases existan en el archivo schemas
from typing import List

router = APIRouter()

procesos_table = Procesos.__table__

@router.post("/", response_model=ProcesoResponse)
async def create_proceso(proceso: ProcesoCreate):
    # Crea un nuevo diccionario para el proceso
    new_proceso = {
        "nombre": proceso.nombre,
        "num_etapas": len(proceso.etapas)
    }
    
    # Inserta el nuevo proceso en la base de datos
    result = conn.execute(procesos_table.insert().values(new_proceso))
    conn.commit()
    
    # Obtiene el último proceso insertado
    proceso_id = result.inserted_primary_key[0]
    
    # Inserta las etapas relacionadas
    for etapa in proceso.etapas:
        new_etapa = {
            "num_etapa": etapa.num_etapa,
            "id_proceso": proceso_id
        }
        etapa_result = conn.execute(Etapas.__table__.insert().values(new_etapa))
        conn.commit()

        etapa_id = etapa_result.inserted_primary_key[0]

        # Inserta las entradas, indicadores y salidas para cada etapa
        for entrada in etapa.entradas:
            conn.execute(EtapasEntradas.__table__.insert().values(id_etapa=etapa_id, id_entrada=entrada.id))
            conn.commit()

        for indicador in etapa.indicadores:
            conn.execute(EtapaIndicadores.__table__.insert().values(id_etapa=etapa_id, id_indicador_entrada=indicador.id))
            conn.commit()

        for salida in etapa.salidas:
            conn.execute(EtapasSalidas.__table__.insert().values(id_etapa=etapa_id, id_entrada=salida.id))
            conn.commit()
    
    # Obtiene el proceso creado con las etapas y detalles completos
    created_proceso = conn.execute(procesos_table.select().where(procesos_table.c.id == proceso_id)).mappings().first()

    return ProcesoResponse.model_validate(created_proceso)
