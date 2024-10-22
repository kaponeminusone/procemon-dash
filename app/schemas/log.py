from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RegistroRead(BaseModel):
    id: int
    id_usuario: int
    descripcion: Optional[str] = None
    creado: datetime
    modificado: datetime
    id_proceso: Optional[int] = None
    id_indicador: Optional[int] = None
    id_entrada: Optional[int] = None
    id_proceso_ejecutado: Optional[int] = None
