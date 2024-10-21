from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db  # Importa la función desde db.py
from app.models.models import Procesos, Usuario, Entradas, Indicadores, Etapas, Registro, RegistroProcesos, RegistroEntradas, RegistroIndicadores
from app.schemas.log import RegistroRead  # Asegúrate de importar tus modelos correctamente
from datetime import datetime, timedelta

router = APIRouter()

# Definición de las tablas
proceso_table = Procesos.__table__
usuario_table = Usuario.__table__
etapas_table = Etapas.__table__
entradas_table = Entradas.__table__
indicadores_table = Indicadores.__table__
registro_table = Registro.__table__
registro_procesos_table = RegistroProcesos.__table__
registro_indicador_table = RegistroIndicadores.__table__
registro_entrada_table = RegistroEntradas.__table__


@router.get("/search/process/", response_model=List[RegistroRead])
async def search_registros_por_proceso(nombre_proceso: str = None, id_proceso: int = None, db: Session = Depends(get_db)):
    query = select(
        registro_table.c.id,
        registro_table.c.id_usuario,
        registro_table.c.descripcion,
        registro_table.c.creado,
        registro_table.c.modificado,
        registro_procesos_table.c.id_proceso
    ).select_from(registro_table)

    if nombre_proceso:
        query = (
            query.join(registro_procesos_table, registro_procesos_table.c.id_registro == registro_table.c.id)
            .join(proceso_table, registro_procesos_table.c.id_proceso == proceso_table.c.id)
            .where(proceso_table.c.nombre.ilike(f'%{nombre_proceso}%'))
        )
    if id_proceso is not None:
        query = (
            query.join(registro_procesos_table, registro_procesos_table.c.id_registro == registro_table.c.id)
            .where(registro_procesos_table.c.id_proceso == id_proceso)
        )

    result = db.execute(query).mappings()
    registros = []
    for row in result:
        registro = RegistroRead.model_validate(row)
        # Añade id_proceso si existe en la consulta
        registro.id_proceso = row.get("id_proceso")
        registros.append(registro)

    if registros:
        return registros
    else:
        raise HTTPException(status_code=404, detail="No se encontraron registros.")

@router.get("/search/indicators/", response_model=List[RegistroRead])
async def search_registros_por_indicador(nombre_indicador: str = None, id_indicador: int = None, db: Session = Depends(get_db)):
    query = select(
        registro_table.c.id,
        registro_table.c.id_usuario,
        registro_table.c.descripcion,
        registro_table.c.creado,
        registro_table.c.modificado,
        registro_indicador_table.c.id_indicador
    ).select_from(registro_table)

    if nombre_indicador:
        query = (
            query.join(registro_indicador_table, registro_indicador_table.c.id_registro == registro_table.c.id)
            .join(indicadores_table, registro_indicador_table.c.id_indicador == indicadores_table.c.id)
            .where(indicadores_table.c.nombre.ilike(f'%{nombre_indicador}%'))
        )
    if id_indicador is not None:
        query = (
            query.join(registro_indicador_table, registro_indicador_table.c.id_registro == registro_table.c.id)
            .where(registro_indicador_table.c.id_indicador == id_indicador)
        )

    result = db.execute(query).mappings()
    registros = []
    for row in result:
        registro = RegistroRead.model_validate(row)
        # Añade id_indicador si existe en la consulta
        registro.id_indicador = row.get("id_indicador")
        registros.append(registro)

    if registros:
        return registros
    else:
        raise HTTPException(status_code=404, detail="No se encontraron registros.")


@router.get("/search/inputs/", response_model=List[RegistroRead])
async def search_registros_por_entrada(nombre_entrada: str = None, id_entrada: int = None, db: Session = Depends(get_db)):
    query = select(
        registro_table.c.id,
        registro_table.c.id_usuario,
        registro_table.c.descripcion,
        registro_table.c.creado,
        registro_table.c.modificado,
        registro_entrada_table.c.id_entrada
    ).select_from(registro_table)

    if nombre_entrada:
        query = (
            query.join(registro_entrada_table, registro_entrada_table.c.id_registro == registro_table.c.id)
            .join(entradas_table, registro_entrada_table.c.id_entrada == entradas_table.c.id)
            .where(entradas_table.c.nombre.ilike(f'%{nombre_entrada}%'))
        )
    if id_entrada is not None:
        query = (
            query.join(registro_entrada_table, registro_entrada_table.c.id_registro == registro_table.c.id)
            .where(registro_entrada_table.c.id_entrada == id_entrada)
        )

    result = db.execute(query).mappings()
    registros = []
    for row in result:
        registro = RegistroRead.model_validate(row)
        # Añade id_entrada si existe en la consulta
        registro.id_entrada = row.get("id_entrada")
        registros.append(registro)

    if registros:
        return registros
    else:
        raise HTTPException(status_code=404, detail="No se encontraron registros.")


@router.get("/search/users/", response_model=List[RegistroRead])
async def search_registros_por_usuario(nombre_usuario: str = None, id_usuario: int = None, db: Session = Depends(get_db)):
    query = select(registro_table)

    if nombre_usuario:
        query = (
            query.join(usuario_table, registro_table.c.id_usuario == usuario_table.c.id)
            .where(usuario_table.c.nombre.ilike(f'%{nombre_usuario}%'))
        )
    if id_usuario is not None:
        query = (
            query.where(registro_table.c.id_usuario == id_usuario)
        )

    result = db.execute(query).mappings()
    registros = [RegistroRead.model_validate(row) for row in result]
    if registros:
        return registros
    else:
        raise HTTPException(status_code=404, detail="No se encontraron registros.")

from sqlalchemy import select, join
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from typing import List

# Asumiendo que has definido las tablas aquí
proceso_table = Procesos.__table__
usuario_table = Usuario.__table__
etapas_table = Etapas.__table__
entradas_table = Entradas.__table__
indicadores_table = Indicadores.__table__
registro_table = Registro.__table__
registro_procesos_table = RegistroProcesos.__table__
registro_indicador_table = RegistroIndicadores.__table__
registro_entrada_table = RegistroEntradas.__table__

@router.get("/search/", response_model=List[RegistroRead])
async def search_registros(
    nombre_proceso: str = None,
    id_proceso: int = None,
    nombre_indicador: str = None,
    id_indicador: int = None,
    nombre_entrada: str = None,
    id_entrada: int = None,
    nombre_usuario: str = None,
    id_usuario: int = None,
    db: Session = Depends(get_db)
):
    query = select(registro_table)

    # Filtrar por proceso
    if nombre_proceso or id_proceso is not None:
        subquery_proceso = select(
            registro_procesos_table.c.id_registro
        ).join(proceso_table)

        if nombre_proceso:
            subquery_proceso = subquery_proceso.where(proceso_table.c.nombre.ilike(f'%{nombre_proceso}%'))
        if id_proceso is not None:
            subquery_proceso = subquery_proceso.where(registro_procesos_table.c.id_proceso == id_proceso)

        # Ejecutar la subconsulta para obtener los resultados
        subquery_proceso_result = db.execute(subquery_proceso).scalars().all()
        if subquery_proceso_result:  # Comprobar si hay resultados
            query = query.where(registro_table.c.id.in_(subquery_proceso_result))

    # Filtrar por indicador
    if nombre_indicador or id_indicador is not None:
        subquery_indicador = select(
            registro_indicador_table.c.id_registro
        ).join(indicadores_table)

        if nombre_indicador:
            subquery_indicador = subquery_indicador.where(indicadores_table.c.nombre.ilike(f'%{nombre_indicador}%'))
        if id_indicador is not None:
            subquery_indicador = subquery_indicador.where(registro_indicador_table.c.id_indicador == id_indicador)

        # Ejecutar la subconsulta para obtener los resultados
        subquery_indicador_result = db.execute(subquery_indicador).scalars().all()
        if subquery_indicador_result:  # Comprobar si hay resultados
            query = query.where(registro_table.c.id.in_(subquery_indicador_result))

    # Filtrar por entrada
    if nombre_entrada or id_entrada is not None:
        subquery_entrada = select(
            registro_entrada_table.c.id_registro
        ).join(entradas_table)

        if nombre_entrada:
            subquery_entrada = subquery_entrada.where(entradas_table.c.nombre.ilike(f'%{nombre_entrada}%'))
        if id_entrada is not None:
            subquery_entrada = subquery_entrada.where(registro_entrada_table.c.id_entrada == id_entrada)

        # Ejecutar la subconsulta para obtener los resultados
        subquery_entrada_result = db.execute(subquery_entrada).scalars().all()
        if subquery_entrada_result:  # Comprobar si hay resultados
            query = query.where(registro_table.c.id.in_(subquery_entrada_result))

    # Filtrar por usuario
    if nombre_usuario or id_usuario is not None:
        subquery_usuario = select(usuario_table.c.id)
        if nombre_usuario:
            subquery_usuario = subquery_usuario.where(usuario_table.c.nombre.ilike(f'%{nombre_usuario}%'))
        if id_usuario is not None:
            subquery_usuario = subquery_usuario.where(usuario_table.c.id == id_usuario)

        # Ejecutar la subconsulta para obtener los resultados
        subquery_usuario_result = db.execute(subquery_usuario).scalars().all()
        if subquery_usuario_result:  # Comprobar si hay resultados
            query = query.where(registro_table.c.id_usuario.in_(subquery_usuario_result))

    result = db.execute(query).mappings()
    registros = [RegistroRead.model_validate(row) for row in result]

    if registros:
        return registros
    else:
        raise HTTPException(status_code=404, detail="No se encontraron registros.")

@router.get("/latest/{size}", response_model=List[RegistroRead])
async def obtener_ultimos_registros(size: int, db: Session = Depends(get_db)):
    # Verifica que la size sea positiva
    if size <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser un número positivo.")

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Calcular la fecha límite para obtener los últimos registros
    fecha_limite = fecha_actual - timedelta(days=size)  # Puedes ajustar esto según lo que necesites

    # Realizar la consulta
    query = select(registro_table).where(registro_table.c.creado >= fecha_limite).order_by(registro_table.c.creado.desc()).limit(size)

    result = db.execute(query).mappings()
    registros = [RegistroRead.model_validate(row) for row in result]

    if registros:
        return registros
    else:
        return []
    
#TODO: TRADUCIR A UN SOLO IDIOMA LOS PARAMETROS