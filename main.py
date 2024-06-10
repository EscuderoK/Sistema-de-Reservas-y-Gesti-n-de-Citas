from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import HTTPException
import schemas
from models import *
from crud import *
from schemas import * 
import models, crud


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


@app.get("/afiliacion/")
def get_ciudades(db: Session = Depends(get_db)):
    return db.query(Afiliacion).all()

@app.get("/paciente/")
def get_ciudades(db: Session = Depends(get_db)):
    return db.query(Pacientes).all()

#Funcionalidades
@app.get("/horario_atencion/")
def get_ciudades(db: Session = Depends(get_db)):
    return db.query(HorarioAtencion).all()

@app.post("/agendar-cita/")
def agendar_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    # Verificar que el horario existe
    horario = db.query(models.HorarioAtencion).filter(models.HorarioAtencion.id_horario == cita.id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    nueva_cita = crud.create_cita(db, id_horario=cita.id_horario, id_paciente=cita.id_paciente, 
                                  id_servicio=cita.id_servicio, id_consultorio=cita.id_consultorio, 
                                  id_profesional=cita.id_profesional)
    return nueva_cita

@app.delete("/cancelar-cita/{id_cita}")
def cancelar_cita(id_cita: int, db: Session = Depends(get_db)):
    cita = crud.delete_cita(db, id_cita)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"detail": "Cita cancelada con éxito"}

@app.put("/reprogramar-cita/{id_cita}")
def reprogramar_cita(id_cita: int, cita: schemas.CitaCreate, db: Session = Depends(get_db)):
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
