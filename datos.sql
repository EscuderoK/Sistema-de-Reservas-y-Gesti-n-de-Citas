CREATE TABLE afiliacion (
	id_afiliacion SERIAL PRIMARY KEY,
	tipo_afiliacion VARCHAR(12)
);

CREATE TABLE eps (
	id_eps SERIAL PRIMARY KEY,
	nombre_eps VARCHAR(30),
	nit INTEGER,
	id_contacto INT REFERENCES contacto(id_contacto)	
);

CREATE TABLE paciente (
	id_paciente SERIAL PRIMARY KEY,
    documento INT,
    tipo_documento VARCHAR(255),
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    genero VARCHAR(255),
    fecha_nacimiento DATE,
	id_eps INT REFERENCES eps(id_eps),
	id_afiliacion INT REFERENCES afiliacion(id_afiliacion),
	id_ciudad INT REFERENCES ciudad(id_ciudad),
	id_contacto INT REFERENCES contacto(id_contacto)	
);

CREATE TABLE profesional (
	id_profesional SERIAL PRIMARY KEY,
	tipo_documento VARCHAR(20),
	nombre VARCHAR(255),
	apellido VARCHAR(255),
	genero VARCHAR(15),
	fecha_nacimiento DATE,
	tarjeta_profesional VARCHAR(255),
	modalidad VARCHAR(15),
	id_ciudad INT REFERENCES ciudad(id_ciudad),
	id_contacto INT REFERENCES contacto(id_contacto),
	id_ips INT REFERENCES ips(id_ips)
	);

ID_Profesional SERIAL PRIMARY KEY,
    Documento INT
    Tipo_Documento VARCHAR(255),
    Nombre VARCHAR(255),
    Apellido VARCHAR(255),
    Genero VARCHAR(255),
    Fecha_Nacimiento DATE,
    Tarjeta_Profesional VARCHAR(255),
    ID_Cuidad INT,
    ID_Servicio INT,
    ID_Contacto INT,
    ID_IPS INT,
    Modalidad VARCHAR(255)

CREATE TABLE contacto (
	id_contacto SERIAL PRIMARY KEY,
	telefono INTEGER,
	celular INTEGER,
	direccion VARCHAR(255),
	barrio VARCHAR(255),
	email VARCHAR(100)
);
	
CREATE TABLE ciudad (
	id_ciudad SERIAL PRIMARY KEY,
	ciudad VARCHAR(50)
);



CREATE TABLE ips (
	id_ips SERIAL PRIMARY KEY,
	nombre_ips VARCHAR(100),
	nit INTEGER,
	clasificacion VARCHAR(30),
	id_ciudad INT REFERENCES ciudad(id_ciudad)
);

ALTER TABLE ips
ADD COLUMN id_eps INT REFERENCES eps(id_eps);

CREATE TABLE servicio(
	id_servicio SERIAL PRIMARY KEY,
	servicio VARCHAR(50),
	id_ips INT REFERENCES ips(id_ips)
	);

CREATE TABLE tarifa (
	id_tarifa SERIAL PRIMARY KEY,
	tarifa INTEGER,
	id_afiliacion INT REFERENCES afiliacion(id_afiliacion),
	id_servicio INT REFERENCES servicio(id_servicio)
)

CREATE TABLE consultorio (
	id_consultorio SERIAL PRIMARY KEY,
	codigo_consultorio VARCHAR(10),
	id_servicio INT REFERENCES servicio(id_servicio)
);

CREATE TABLE horario_atencion (
	id_horario SERIAL PRIMARY KEY,
	fecha DATE,
	hora_inicio TIMESTAMP,
	hora_fin TIMESTAMP,
	id_consultorio INT REFERENCES consultorio(id_consultorio)	
);

CREATE TABLE agendar_cita(
	id_cita SERIAL PRIMARY KEY,
	id_horario INT REFERENCES horario_atencion(id_horario),
	id_paciente INT REFERENCES paciente(id_paciente),
	id_servicio INT REFERENCES servicio (id_servicio),
	id_consultorio INT REFERENCES consultorio(id_consultorio),
	id_profesional INT REFERENCES profesional(id_profesional)
	);

CREATE TABLE historial_estado(
	id_historial SERIAL PRIMARY KEY,
	estado INTEGER,
	fecha_modificacion DATE,
	hora_modificacion TIMESTAMP,
	observacion VARCHAR(100),
	id_horario INT REFERENCES horario_atencion(id_horario),
	id_cita INT REFERENCES agendar_cita(id_cita),
	id_paciente INT REFERENCES paciente(id_paciente),
	id_profesional INT REFERENCES profesional(id_profesional)
);

CREATE TABLE recordatorio(
	id_recordatorio SERIAL PRIMARY KEY,
	id_cita INT REFERENCES agendar_cita(id_cita),
	id_servicio INT REFERENCES servicio(id_servicio),
	id_paciente INT REFERENCES paciente(id_paciente),
	id_contacto INT REFERENCES contacto(id_contacto),
	id_profesional INT REFERENCES profesional(id_profesional),
	fecha_cita DATE,
	hora_cita TIMESTAMP,
	mensaje VARCHAR(255)
	);

-- Ingreso de datos a nuestras tablas
INSERT INTO afiliacion(id_afiliacion,tipo_afiliacion)
(1,'Contributivo'),
(2,'Subsidiado'),
(3,'Beneficiario')

INSERT INTO paciente(id_paciente, documento, tipo_documento, nombre, apellido,
					 genero, fecha_nacimiento, id_eps, id_afiliacion, id_ciudad, id_contacto)
VALUES
(1, '12345678', 'CC', 'Juan', 'Pérez', 'M', '1990-05-21', 1, 1, 11001, 101),
(2, '23456789', 'CC', 'María', 'Gómez', 'F', '1985-03-14', 2, 2, 11001, 102),
(3, '34567890', 'TI', 'Carlos', 'Rodríguez', 'M', '2000-11-30', 3, 3, 5001, 103),
(4, '45678901', 'CC', 'Ana', 'Martínez', 'F', '1995-07-12', 1, 2, 5001, 101),
(5, '56789012', 'CC', 'Luis', 'Hernández', 'M', '1982-09-19', 2, 1, 76001, 102),
(6, '67890123', 'TI', 'Laura', 'García', 'F', '2003-01-25', 3, 3, 76001, 103),
(7, '78901234', 'CC', 'Jorge', 'López', 'M', '1998-06-14', 1, 1, 11001, 101),
(8, '89012345', 'CC', 'Elena', 'Sánchez', 'F', '1993-02-28', 2, 2, 11001, 101),
(9, '90123456', 'TI', 'David', 'Ramírez', 'M', '2002-12-10', 3, 3, 5001, 102),
(10, '01234567', 'CC', 'Marta', 'Cruz', 'F', '1987-04-05', 1, 1, 5001, 103),
(11, '12345000', 'CC', 'Andrés', 'Castro', 'M', '1994-08-22', 2, 2, 5001, 103),
(12, '23456000', 'CC', 'Isabel', 'Jiménez', 'F', '1991-03-07', 3, 1, 5001, 102),
(13, '34567000', 'TI', 'Ricardo', 'Torres', 'M', '1999-11-15', 1, 3, 11001, 101),
(14, '45678000', 'CC', 'Sandra', 'Morales', 'F', '1983-06-23', 2, 1, 11001, 102),
(15, '56789001', 'CC', 'Pedro', 'Rojas', 'M', '1986-10-19', 3, 2, 11001, 103),
(16, '67890012', 'TI', 'Claudia', 'Gutiérrez', 'F', '2004-05-30', 1, 3, 76001, 101),
(17, '78900123', 'CC', 'Felipe', 'Díaz', 'M', '1997-09-18', 2, 1, 76001, 101),
(18, '89001234', 'CC', 'Natalia', 'Suárez', 'F', '1992-12-14', 3, 2, 76001, 102),
(19, '90102345', 'TI', 'Héctor', 'Ortiz', 'M', '2001-07-20', 1, 3, 76001, 102),
(20, '01203456', 'CC', 'Luisa', 'Blanco', 'F', '1989-11-11', 2, 2, 5001, 103);

INSERT INTO profesional(id_profesional, tipo_documento, nombre, apellido,
                        genero, fecha_nacimiento, tarjeta_profesional, modalidad,
                        id_ciudad, id_contacto, id_ips)
VALUES
(10, 'CC', 'Natalia', 'Perez', 'F', '1992-12-14', '89001231', 'Presencial', 5001, 201, 1),
(20, 'CC', 'Héctor', 'Jimenez', 'M', '2001-07-20', '90102342', 'Presencial', 5001, 202, 1),
(30,  'CC', 'Luisa', 'Gutierrez', 'F', '1989-11-11', '01203453', 'Virtual', 5001, 203, 1);

INSERT INTO servicio(id_servicio,servicio,id_ips)
VALUES
(1,'Medicinal general presencial',9),
(2,'Oftamologia',10),
(3,'Odontologia',11);

INSERT INTO tarifa(id_tarifa,tarifa,id_afiliacion,id_servicio)
VALUES
(300,5000,1,1),
(301,5000,2,1),
(302,3000,3,1),
(303,7000,1,2),
(304,7000,2,2),
(305,5000,3,2),
(306,7000,1,3),
(307,7000,2,3),
(308,5000,3,3)

INSERT INTO consultorio(id_consultorio, codigo_consultorio, id_servicio)
VALUES
(120, 120, 1),
(122, 122, 2),
(124, 124, 3);

INSERT INTO horario_atencion (id_horario, fecha, hora_inicio, hora_fin, id_consultorio)
VALUES 
(08, '2024-06-10', '08:00', '08:30', 120),
(09, '2024-06-10', '09:00', '09:30', 120),
(10, '2024-06-10', '10:00', '10:30', 120),
(11, '2024-06-10', '11:00', '11:30', 120)