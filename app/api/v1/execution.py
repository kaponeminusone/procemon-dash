from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import ProcesosEjecutados, Materiales, Registro, RegistroProcesoEjecutado, RegistroProcesos
from app.schemas.execution import EjecucionProcesoSchema, EtapaRegistroSchema, MaterialSchema, RegistroEjecucionSchema
import random
import json
import os

router = APIRouter()

# Variables de tablas para evitar el uso de __table__ directamente
procesos_ejecutados_table = ProcesosEjecutados.__table__
materiales_table = Materiales.__table__
registro_table = Registro.__table__
registro_procesos_ejecutados_table = RegistroProcesoEjecutado.__table__

def guardar_en_json(data: List[dict], filename: str):
    """Guarda los datos en un archivo JSON."""
    print("Guardando en Json?")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def crear_registro_proceso(db: Session, proceso_id: int, descripcion: str, usuario_id: int = 0):
    """Crea un registro de proceso y asocia el registro a un ID de usuario."""
    new_registro = {
        "id_usuario": usuario_id,
        "descripcion": descripcion
    }
    result_registro = db.execute(registro_table.insert().values(new_registro))
    registro_id = result_registro.inserted_primary_key[0]
    
    new_registro_proceso = {
        "id_registro": registro_id,
        "id_proceso_ejecutado": proceso_id
    }
    db.execute(registro_procesos_ejecutados_table.insert().values(new_registro_proceso))

def actualizar_materiales(db: Session, materiales: List[MaterialSchema], es_entrada: bool):
    """Actualiza los materiales en función de las entradas o salidas."""
    for material in materiales:
        
        existing_material = db.execute(materiales_table.select().where(materiales_table.c.id_entrada == material.id)).first()
        
        if not existing_material:

            new_material = {
                "id_entrada": material.id,
                "cantidad_entrada": 0,
                "cantidad_salida": 0,
                "usos": 0,
            }
            db.execute(materiales_table.insert().values(new_material))

        existing_material = db.execute(materiales_table.select().where(materiales_table.c.id_entrada == material.id)).first()
        
        if es_entrada:
            db.execute(materiales_table.update().where(materiales_table.c.id_entrada == material.id).values(
                    cantidad_entrada=existing_material.cantidad_entrada + material.value,
                    usos=existing_material.usos + 1))
        else:
            db.execute(materiales_table.update().where(materiales_table.c.id_entrada == material.id).values(
                    cantidad_salida=existing_material.cantidad_salida + material.value,
                    usos=existing_material.usos + 1))    
            

@router.post("/")
async def execute_proceso(data: EjecucionProcesoSchema, db: Session = Depends(get_db)):
    

    """Ejecuta un proceso y guarda los resultados."""
    # Inicia una transacción
    with db.begin():  # Esto asegura que todo se ejecute como una transacción
        id_proceso = data.id_proceso
        etapas = data.etapas

        # Generar datos aleatorios
        num_etapas_con_conformidades = random.randint(1, 10)
        tasa_de_exito = random.uniform(0.0, 100.0)
        no_conformidades = random.randint(0, 5)
        conformidades = random.randint(0, 5)

        # Crear un registro en ProcesosEjecutados
        new_proceso_ejecutado = {
            "id_proceso": id_proceso,
            "num_etapas_con_conformidades": num_etapas_con_conformidades,
            "tasa_de_exito": tasa_de_exito,
            "no_conformidades": no_conformidades,
            "conformidades": conformidades
        }

        proceso_ejecutado = db.execute(procesos_ejecutados_table.insert().values(new_proceso_ejecutado))
        
        # Guardar datos en la tabla de Materiales (entradas y salidas)
        
        for etapa in etapas:
            actualizar_materiales(db, etapa.entradas, es_entrada=True)
            actualizar_materiales(db, etapa.salidas, es_entrada=False)

        # Construir los datos para guardar en JSON

        data_to_save = {
            "id_proceso": id_proceso,
            "id_proceso_ejecutado": proceso_ejecutado.inserted_primary_key[0],
            "num_etapas": len(etapas),
            "no_conformes": no_conformidades,
            "conformes": conformidades,
            "etapas": []
        }

        for etapa in etapas:
            etapa_data = {
                "num_etapa": etapa.num_etapa,
                "conformes": random.randint(0, 5), #etapa.conformes,
                "no_conformes": random.randint(0, 5),#etapa.no_conformidades,
                "state": bool(random.randint(0,1)), #etapa.state
                "entradas": [entrada.model_dump() for entrada in etapa.entradas],
                "indicadores": [indicador.model_dump() for indicador in etapa.indicadores],
                "salidas": [salida.model_dump() for salida in etapa.salidas]
            }
            data_to_save["etapas"].append(etapa_data)

        RegistroEjecucionSchema.model_validate(data_to_save)
        # Guardar en JSON
        guardar_en_json([data_to_save], 'data/data_procesos.json')

        # Crear el registro de proceso
        descripcion = f"Ejecución ID {data_to_save["id_proceso_ejecutado"]} de proceso ID {data_to_save['id_proceso']} con {len(etapas)} etapas."
        crear_registro_proceso(db, data_to_save["id_proceso_ejecutado"], descripcion)

    return {"message": "Proceso ejecutado y datos guardados."}
