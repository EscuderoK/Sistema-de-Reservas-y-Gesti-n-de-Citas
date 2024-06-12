from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class AsistenteRequest(BaseModel):
    mensaje: str
    
class CitaBase(BaseModel):
    id_horario: int
    id_paciente: int
    id_servicio: int
    id_consultorio: int
    id_profesional: int

class CitaCreate(CitaBase):
    pass

class Cita(CitaBase):
    id: int

    class Config:
        from_attributes = True

