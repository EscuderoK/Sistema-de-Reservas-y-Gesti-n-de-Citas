import models
from sqlalchemy.orm import Session
from models import *

"Creación de la cita"
def create_cita(db: Session, id_horario: int, id_paciente: int, id_servicio: int, id_consultorio: int, 
                id_profesional: int):
    nueva_cita = models.AgendarCita(id_horario=id_horario, id_paciente=id_paciente, id_servicio=id_servicio, 
                                    id_consultorio=id_consultorio, id_profesional=id_profesional)
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

"Cancelación de la cita"
def delete_cita(db: Session, id_cita: int):
    cita = db.query(models.AgendarCita).filter(models.AgendarCita.id_cita == id_cita).first()
    if not cita:
        return None
    db.delete(cita)
    db.commit()
    return cita

"Reprogramación de la cita"
def update_cita(db: Session, id_cita: int, id_horario: int, id_servicio: int, id_consultorio: int, id_profesional: int):
    cita = db.query(models.AgendarCita).filter(models.AgendarCita.id_cita == id_cita).first()
    if not cita:
        return None
    cita.id_horario = id_horario
    cita.id_servicio = id_servicio
    cita.id_consultorio = id_consultorio
    cita.id_profesional = id_profesional
    db.commit()
    db.refresh(cita)
    return cita
