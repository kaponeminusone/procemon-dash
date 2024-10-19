from pydantic import BaseModel
from typing import List, Optional

class EntradaBase(BaseModel):
    id: int

class IndicadorBase(BaseModel):
    id: int
    entrada_id: int  # ID de la entrada que evalúa

class SalidaBase(BaseModel):
    id: int

class EtapaCreate(BaseModel):
    num_etapa: int
    entradas: List[EntradaBase]
    indicadores: List[IndicadorBase]
    salidas: List[SalidaBase]

class ProcesoCreate(BaseModel):
    nombre: str
    etapas: List[EtapaCreate]


class EntradaResponse(BaseModel):
    id: int
    nombre: str
    tipo: str  # Asumiendo que tienes un campo "tipo" en el modelo Entradas

class IndicadorResponse(BaseModel):
    id: int
    nombre: str  # Asumiendo que tienes un campo "nombre" en el modelo Indicadores
    tipo: str  # Asumiendo que tienes un campo "tipo" en el modelo Indicadores
    entrada_id: int

class SalidaResponse(BaseModel):
    id: int
    nombre: str  # Asumiendo que tienes un campo "nombre" en el modelo Entradas
    tipo: str  # Asumiendo que tienes un campo "tipo" en el modelo Entradas

class EtapaResponse(BaseModel):
    id: int
    num_etapa: int
    entradas: List[EntradaResponse]
    indicadores: List[IndicadorResponse]
    salidas: List[SalidaResponse]

class ProcesoResponse(BaseModel):
    id: int
    nombre: str
    num_etapas: int
    etapas: List[EtapaResponse]
