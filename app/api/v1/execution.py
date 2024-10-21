from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import ProcesosEjecutados, Materiales, Registro, RegistroProcesos
from app.schemas.execution import EjecucionProcesoSchema, EtapaRegistroSchema, MaterialSchema
import random
import json
import os

router = APIRouter()

# Variables de tablas para evitar el uso de __table__ directamente
procesos_ejecutados_table = ProcesosEjecutados.__table__
materiales_table = Materiales.__table__
registro_table = Registro.__table__
registro_procesos_table = RegistroProcesos.__table__

def guardar_en_json(data: List[dict], filename: str):
    """Guarda los datos en un archivo JSON."""
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
        "id_proceso": proceso_id
    }
    db.execute(registro_procesos_table.insert().values(new_registro_proceso))

def actualizar_materiales(db: Session, materiales: List[MaterialSchema], es_entrada: bool):
    """Actualiza los materiales en función de las entradas o salidas."""
    for material in materiales:
        existing_material = db.execute(materiales_table.select().where(materiales_table.c.id_entrada == material.id)).first()
        if existing_material:
            if es_entrada:
                db.execute(materiales_table.update().where(materiales_table.c.id_entrada == material.id).values(
                    cantidad_entrada=existing_material.cantidad_entrada + material.value))
            else:
                db.execute(materiales_table.update().where(materiales_table.c.id_entrada == material.id).values(
                    cantidad_salida=existing_material.cantidad_salida + material.value))
        else:
            new_material = {
                "id_entrada": material.id,
                "cantidad_entrada": material.value if es_entrada else 0,
                "cantidad_salida": material.value if not es_entrada else 0
            }
            db.execute(materiales_table.insert().values(new_material))

@router.post("/")
async def execute_proceso(data: EjecucionProcesoSchema, db: Session = Depends(get_db)):
    
    print(data.model_dump_json(indent=4)) #FUNCIONA BIEN, LO DEMAS ESTÁ DUDOSO

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
            "id_proceso": proceso_ejecutado.inserted_primary_key[0],
            "num_etapas_con_conformidades": num_etapas_con_conformidades,
            "tasa_de_exito": tasa_de_exito,
            "no_conformidades": no_conformidades,
            "conformidades": conformidades,
            "etapas": []
        }

        for etapa in etapas:
            etapa_data = {
                "num_etapa": etapa.num_etapa,
                "conformes": etapa.conformes,
                "no_conformes": etapa.no_conformidades,
                "state": etapa.state,
                "entradas": [entrada.dict() for entrada in etapa.entradas],
                "indicadores": [indicador.dict() for indicador in etapa.indicadores],
                "salidas": [salida.dict() for salida in etapa.salidas]
            }
            data_to_save["etapas"].append(etapa_data)

        # Guardar en JSON
        guardar_en_json([data_to_save], 'data/data_procesos.json')

        # Crear el registro de proceso
        descripcion = f"Ejecución de proceso ID {data_to_save['id_proceso']} con {num_etapas_con_conformidades} etapas."
        crear_registro_proceso(db, data_to_save['id_proceso'], descripcion)

    return {"message": "Proceso ejecutado y datos guardados."}
