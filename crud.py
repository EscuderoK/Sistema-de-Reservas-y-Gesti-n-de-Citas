import models
from sqlalchemy.orm import Session
from models import *

def create_cita(db: Session, id_horario: int, id_paciente: int, id_servicio: int, id_consultorio: int, 
                id_profesional: int):
    """
    Crea una nueva cita en la base de datos.

    Args:
    - db (Session): La sesión de la base de datos.
    - id_horario (int): El ID del horario de atención para la cita.
    - id_paciente (int): El ID del paciente para la cita.
    - id_servicio (int): El ID del servicio para la cita.
    - id_consultorio (int): El ID del consultorio para la cita.
    - id_profesional (int): El ID del profesional para la cita.

    Returns:
    - models.AgendarCita: La cita creada.
    """
    nueva_cita = models.AgendarCita(id_horario=id_horario, id_paciente=id_paciente, id_servicio=id_servicio, 
                                    id_consultorio=id_consultorio, id_profesional=id_profesional)
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita


def delete_cita(db: Session, id_cita: int):
    """
    Elimina una cita de la base de datos.

    Args:
    - db (Session): La sesión de la base de datos.
    - id_cita (int): El ID de la cita a eliminar.

    Returns:
    - models.AgendarCita: La cita eliminada, o None si no se encontró ninguna cita con el ID dado.
    """
    cita = db.query(models.AgendarCita).filter(models.AgendarCita.id_cita == id_cita).first()
    if not cita:
        return None
    db.delete(cita)
    db.commit()
    return cita


def update_cita(db: Session, id_cita: int, id_horario: int, id_servicio: int, id_consultorio: int, id_profesional: int):
    """
    Actualiza los detalles de una cita en la base de datos.

    Args:
    - db (Session): La sesión de la base de datos.
    - id_cita (int): El ID de la cita a actualizar.
    - id_horario (int): El nuevo ID de horario para la cita.
    - id_servicio (int): El nuevo ID de servicio para la cita.
    - id_consultorio (int): El nuevo ID de consultorio para la cita.
    - id_profesional (int): El nuevo ID de profesional para la cita.

    Returns:
    - models.AgendarCita: La cita actualizada, o None si no se encontró ninguna cita con el ID dado.
    """
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

