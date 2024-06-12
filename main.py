from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import HTTPException
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
@app.post("/asistente/")
def asistente_ia(request: AsistenteRequest, db: Session = Depends(get_db)):
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
            if horario_atencion:
                respuesta = "Estos son los horarios disponibles:\n"
                for horarios in horario_atencion:
                    respuesta += f" El dia {horarios.fecha} - a las {horarios.hora_inicio} - en el consultorio {horarios.id_consultorio}\n"
            else: 
                respuesta = "No hay citas disponibles en este momento"
    return {"respuesta": respuesta}
#-----------------------





#Funcionalidades

@app.post("/agendar-cita/")
def agendar_cita(cita: schemas.CitaCreate, db: Session = Depends(get_db)):
    """
    Agendar una nueva cita.

    Verifica si el horario existe, crea una nueva cita y elimina el horario correspondiente.

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
    
    # Crear la nueva cita
    nueva_cita = crud.create_cita(db, id_horario=cita.id_horario, id_paciente=cita.id_paciente, 
                                  id_servicio=cita.id_servicio, id_consultorio=cita.id_consultorio, 
                                  id_profesional=cita.id_profesional)
    # Eliminar el horario
    db.delete()
    db.commit()
    
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

@app.put("/reprogramar-cita/{id_cita}")
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
    horario = db.query(models.HorarioAtencion).filter(models.HorarioAtencion.id_horario == cita.id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    cita_actualizada = crud.update_cita(db, id_cita=id_cita, id_horario=cita.id_horario, id_servicio=cita.id_servicio, 
                                        id_consultorio=cita.id_consultorio, id_profesional=cita.id_profesional)
    if not cita_actualizada:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita_actualizada

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
