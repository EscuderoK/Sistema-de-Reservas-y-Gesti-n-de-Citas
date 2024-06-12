from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
class Afiliacion(Base):
    __tablename__ = 'afiliacion'
    id_afiliacion = Column(Integer, primary_key=True, index=True)
    tipo_afiliacion = Column(String, index=True)

class Ciudades(Base):
    __tablename__ = 'ciudad'
    id_ciudad = Column(Integer, primary_key=True, index=True)
    ciudad = Column(String, index=True)

class Contactos(Base):
    __tablename__ = 'contacto'
    id_contacto = Column(Integer, primary_key=True, index=True)
    telefono = Column(Integer)
    celular = Column(Integer)
    direccion = Column(String)
    barrio = Column(String)
    email = Column(String)



class Eps(Base):
    __tablename__ = 'eps'
    id_eps = Column(Integer, primary_key=True, index=True)
    nombre_eps = Column(String)
    nit = Column(Integer)
    id_contacto = Column(Integer, ForeignKey('contacto.id_contacto'))

class Ips(Base):
    __tablename__ = 'ips'
    id_ips = Column(Integer, primary_key=True, index=True)
    nombre_ips = Column(String)
    nit = Column(Integer)
    clasificacion = Column(String)
    id_ciudad = Column(Integer, ForeignKey('ciudad.id_ciudad'))
    id_eps = Column(Integer, ForeignKey('eps.id_eps'))

class Pacientes(Base):
    __tablename__ = 'paciente'
    id_paciente = Column(Integer, primary_key=True, index=True)
    documento = Column(String, index=True)
    tipo_documento = Column(String)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    genero = Column(String)
    fecha_nacimiento = Column(Date)
    id_eps = Column(Integer, ForeignKey('eps.id_eps'))
    id_afiliacion = Column(Integer, ForeignKey('afiliacion.id_afiliacion'))
    id_ciudad = Column(Integer, ForeignKey('ciudad.id_ciudad'))
    id_contacto = Column(Integer, ForeignKey('contacto.id_contacto'))

class Profesional(Base):
    __tablename__ = 'profesional'
    id_profesional = Column(Integer, primary_key=True, index=True)
    tipo_documento = Column(String)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    genero = Column(String)
    fecha_nacimiento = Column(Date)
    tarjeta_profesional = Column(String, index=True)
    modalidad = Column(String)
    id_ciudad = Column(Integer, ForeignKey('ciudad.id_ciudad'))
    id_contacto = Column(Integer, ForeignKey('contacto.id_contacto'))
    id_ips = Column(Integer, ForeignKey('ips.id_ips'))

class Servicio(Base):
    __tablename__ = 'servicio'
    id_servicio = Column(Integer, primary_key=True, index=True)
    servicio = Column(String, index=True)
    id_ips = Column(Integer, ForeignKey('ips.id_ips'))

class Tarifa(Base):
    __tablename__ = 'tarifa'
    id_tarifa = Column(Integer, primary_key=True, index=True)
    tarifa = Column(String, index=True)
    id_afiliacion = Column(Integer, ForeignKey('afiliacion.id_afiliacion'))
    id_servicio = Column(Integer, ForeignKey('servicio.id_servicio'))

class AgendarCita(Base):
    __tablename__ = 'agendar_cita'
    id_cita = Column(Integer, primary_key=True, index=True)
    id_horario = Column(Integer, ForeignKey('horario_atencion.id_horario'))
    id_paciente = Column(Integer, ForeignKey('paciente.id_paciente'))
    id_servicio = Column(Integer, ForeignKey('servicio.id_servicio'))
    id_consultorio = Column(Integer, ForeignKey('consultorio.id_consultorio'))
    id_profesional = Column(Integer, ForeignKey('profesional.id_profesional'))

class Consultorio(Base):
    __tablename__ = 'consultorio'
    id_consultorio = Column(Integer, primary_key=True, index=True)
    codigo_consultorio = Column(String, index=True)
    id_servicio = Column(Integer, ForeignKey('servicio.id_servicio'))

class HistorialEstado(Base):
    __tablename__ = 'historial_estado'
    id_historial = Column(Integer, primary_key=True, index=True)
    estado = Column(String, index=True)
    fecha_modificacion = Column(Date)
    hora_modificacion = Column(String)
    observacion = Column(String)
    id_horario = Column(Integer, ForeignKey('horario_atencion.id_horario'))
    id_cita = Column(Integer, ForeignKey('agendar_cita.id_cita'))
    id_paciente = Column(Integer, ForeignKey('paciente.id_paciente'))
    id_profesional = Column(Integer, ForeignKey('profesional.id_profesional'))

class HorarioAtencion(Base):
    __tablename__ = 'horario_atencion'
    id_horario = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    hora_inicio = Column(String)
    hora_fin = Column(String)
    id_consultorio = Column(Integer, ForeignKey('consultorio.id_consultorio'))

class Recordatorio(Base):
    __tablename__ = 'recordatorio'
    id_recordatorio = Column(Integer, primary_key=True, index=True)
    id_cita = Column(Integer, ForeignKey('agendar_cita.id_cita'))
    id_paciente = Column(Integer, ForeignKey('paciente.id_paciente'))
    id_contacto = Column(Integer, ForeignKey('contacto.id_contacto'))
    id_profesional = Column(Integer, ForeignKey('profesional.id_profesional'))
    fecha_cita = Column(Date)
    hora_cita = Column(String)
    mensaje = Column(String)