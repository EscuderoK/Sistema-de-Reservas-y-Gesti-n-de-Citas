from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import schemas
from models import *
from crud import *
from schemas import * 
import openai
import models, crud
openai.api_key = "Tsk-proj-bZTt9dmrNO146CsZzGguT3BlbkFJZza6zilOwIAxXXwIM6L2"
import logging


app = FastAPI()

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        logger.debug("Connection to database established")
        yield db
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Sistema Reservas"}

#-----------------------
# Ruta para el asistente de IA
@app.post("/asistente/", summary="Asistente Virtual", description="Asistente para gestionar dudas de los pacientes")
def asistente_ia(request: AsistenteRequest, db: Session = Depends(get_db)):
    """
    Asistente Virtual

    Gestiona las dudas de los pacientes con el asistente virtual.

    - Si el mensaje contiene "agendar cita", el asistente solicitará el motivo y horario de la cita.
    - Si el mensaje contiene "mostrar servicios disponibles" o "servicios disponibles", el asistente mostrará los servicios disponibles.
    - Si el mensaje contiene "quiero agendar una cita" o "ver horarios disponibles", el asistente mostrará los horarios disponibles para agendar una cita.

    Args:
        - request (AsistenteRequest): Información de la solicitud del asistente.
        - db (Session): Sesión de la base de datos.

    Returns:
        - Dict: Respuesta del asistente virtual.
    """
    mensaje = request.mensaje.lower()
    respuesta = "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"

    if "agendar cita" in mensaje:
        respuesta = "Entendido, ¿cuál es el motivo de la cita y en qué horario te gustaría agendarla?"
    elif "mostrar servicios disponibles" in mensaje or "servicios disponibles" in mensaje:
        servicios = db.query(models.Servicio).all()
        if servicios:
            respuesta = "Estos son los servicios disponibles:\n"
            for servicio in servicios:
                respuesta += f"{servicio.id_servicio} - {servicio.servicio}\n"
        else:
            respuesta = "No hay servicios disponibles en este momento."
    elif "quiero agendar una cita" in mensaje or "ver horarios disponibles" in mensaje:
            horario_atencion = db.query(models.HorarioAtencion).all()
            respuesta = [
                horario for horario in horario_atencion
                if not db.query(models.AgendarCita).filter(models.AgendarCita.id_horario == horario.id_horario).first()
                ]
            if not respuesta:
                raise HTTPException(status_code=404, detail="No hay horarios disponibles en este momento")
    return {"respuesta": respuesta}
#-----------------------


#Funcionalidades

@app.post("/agendar-cita/")
def agendar_cita(cita: schemas.CitaCreate, db: Session = Depends(get_db)):
    """
    Agendar una nueva cita.

    Verifica si el horario existe y si está disponible, crea una nueva cita y elimina el horario correspondiente.

    Args:
        - cita (CitaCreate): Información de la cita a crear.
        - db (Session): Sesión de la base de datos.

    Returns:
        - Cita: La cita creada.
    """

    # Verificar que el horario existe
    horario = db.query(models.HorarioAtencion).filter(models.HorarioAtencion.id_horario == cita.id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    # Verificar que el horario esté disponible
    cita_existente = db.query(models.AgendarCita).filter(
        models.AgendarCita.id_horario == cita.id_horario
    ).first()
    if cita_existente:
        raise HTTPException(status_code=400, detail="El horario no está disponible")

    # Crear la nueva cita
    nueva_cita = crud.create_cita(
        db, id_horario=cita.id_horario, id_paciente=cita.id_paciente, 
        id_servicio=cita.id_servicio, id_consultorio=cita.id_consultorio, 
        id_profesional=cita.id_profesional
    )

    return {
        "message": "Cita agendada con éxito",
        "cita": nueva_cita
    }



@app.delete("/cancelar-cita/{id_cita}")
def cancelar_cita(id_cita: int, db: Session = Depends(get_db)):
    """
    Cancelar una cita existente.

    Args:
    - id_cita (int): ID de la cita a cancelar.
    - db (Session): Sesión de la base de datos.

    Returns:
    - dict: Detalle de la operación.
    """
    cita = crud.delete_cita(db, id_cita)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"detail": "Cita cancelada con éxito"}

@app.put("/reprogramar-cita/{id_cita}", summary="Reprogramar cita", description="Reprograma una cita existente.")
def reprogramar_cita(id_cita: int, cita: schemas.CitaCreate, db: Session = Depends(get_db)):
    """
    Reprogramar una cita existente.

    Verifica si el nuevo horario existe y actualiza la cita con los nuevos datos.

    Args:
        - id_cita (int): ID de la cita a reprogramar.
        - cita (CitaCreate): Nuevos datos de la cita.
        - db (Session): Sesión de la base de datos.

    Returns:
        - Cita: La cita actualizada.
    """
    # Verificar que el nuevo horario existe
    nuevo_horario = db.query(models.HorarioAtencion).filter(models.HorarioAtencion.id_horario == cita.id_horario).first()
    if not nuevo_horario:
        raise HTTPException(status_code=404, detail="El nuevo horario no encontrado")

    # Verificar que el nuevo horario esté disponible
    cita_existente = db.query(models.AgendarCita).filter(
        models.AgendarCita.id_horario == cita.id_horario
    ).first()
    if cita_existente:
        raise HTTPException(status_code=400, detail="El nuevo horario no está disponible")

    # Actualizar la cita con el nuevo horario
    cita_actualizada = crud.update_cita(
        db, id_cita=id_cita, id_horario=cita.id_horario, id_servicio=cita.id_servicio, 
        id_consultorio=cita.id_consultorio, id_profesional=cita.id_profesional
    )

    if not cita_actualizada:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    return {
        "message": "Cita reprogramada con éxito",
        "cita": cita_actualizada
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
