CREATE DATABASE IF NOT EXISTS mates;
USE mates;

-- =======================================================
-- 1. AUTENTICACION Y PERSONAS
-- =======================================================

CREATE TABLE IF NOT EXISTS Adm_Persona (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    Nombres VARCHAR(100),
    Apellidos VARCHAR(100),
    Dni VARCHAR(8),
    FechaNacimiento DATE,
    Email VARCHAR(150),
    EstudioNivel VARCHAR(50), -- Primaria, Secundaria, Universidad
    Institucion VARCHAR(150),
    -- System Fields
    ESTADO BIT DEFAULT 1,
    FECHA_CREACION BIGINT,
    FECHA_MODIFICACION BIGINT,
    USER_CREACION VARCHAR(50),
    USER_MODIFICACION VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Seg_Jugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdPersona CHAR(36),
    Username VARCHAR(50) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL, -- Storing plain for dev for now as per previous setup
    FechaRegistro BIGINT,
    EstadoCuenta VARCHAR(20) DEFAULT 'ACTIVO', -- ACTIVO, SUSPENDIDO
    -- System Fields
    ESTADO BIT DEFAULT 1,
    FECHA_CREACION BIGINT,
    FECHA_MODIFICACION BIGINT,
    USER_CREACION VARCHAR(50),
    USER_MODIFICACION VARCHAR(50),
    FOREIGN KEY (IdPersona) REFERENCES Adm_Persona(Id)
);

-- =======================================================
-- 2. ESTADISTICAS Y PROGRESION
-- =======================================================

CREATE TABLE IF NOT EXISTS Gam_Temporada (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    Nombre VARCHAR(50), -- "2025-Q1"
    FechaInicio DATE,
    FechaFin DATE,
    ESTADO BIT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Gam_RangoJugadorTemporada (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    IdTemporada CHAR(36) NOT NULL,
    Rango VARCHAR(20), -- BRONCE, PLATA, ORO
    PuntosTemporada INT DEFAULT 0,
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id),
    FOREIGN KEY (IdTemporada) REFERENCES Gam_Temporada(Id)
);

CREATE TABLE IF NOT EXISTS Gam_ExperienciaJugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    TotalExp INT DEFAULT 0,
    ExpPorCurso JSON, -- Flexible storage
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id)
);

CREATE TABLE IF NOT EXISTS Gam_PuntajeJugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    PuntajeTotal INT DEFAULT 0,
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id)
);

CREATE TABLE IF NOT EXISTS Gam_RachaJugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    RachaActual INT DEFAULT 0,
    RachaMaxima INT DEFAULT 0,
    UltimoIngreso DATE,
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id)
);

CREATE TABLE IF NOT EXISTS Gam_DesafioJugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    FocoPrincipal VARCHAR(100),
    Contenido JSON,
    Estado VARCHAR(20), -- PENDIENTE, COMPLETADO
    FechaAsignacion DATE,
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id)
);

-- =======================================================
-- 3. CURSOS Y CONTENIDO
-- =======================================================

CREATE TABLE IF NOT EXISTS Edu_Curso (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion TEXT,
    Rama VARCHAR(50), -- Algebra, Geometria
    Nivel VARCHAR(20), -- BASICO, INTERMEDIO, AVANZADO
    UrlImagen VARCHAR(255),
    ESTADO BIT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Edu_TemaCurso (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdCurso CHAR(36) NOT NULL,
    Nombre VARCHAR(100),
    Descripcion TEXT,
    FOREIGN KEY (IdCurso) REFERENCES Edu_Curso(Id)
);

CREATE TABLE IF NOT EXISTS Edu_ExamenCurso (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdCurso CHAR(36) NOT NULL,
    Preguntas JSON,
    NotaMinima INT DEFAULT 70,
    FOREIGN KEY (IdCurso) REFERENCES Edu_Curso(Id)
);

CREATE TABLE IF NOT EXISTS Edu_RecursoCurso (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdCurso CHAR(36) NOT NULL,
    Tipo VARCHAR(20), -- FORMULA, PISTA
    Contenido TEXT,
    FOREIGN KEY (IdCurso) REFERENCES Edu_Curso(Id)
);

CREATE TABLE IF NOT EXISTS Edu_OperacionMatematica (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdCurso CHAR(36),
    Nombre VARCHAR(50), -- +, -, Integral
    FuncionSistema VARCHAR(100),
    Formula TEXT,
    Atributos JSON
);

CREATE TABLE IF NOT EXISTS Edu_MetodoResolucion (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdOperacion CHAR(36) NOT NULL,
    Nombre VARCHAR(100),
    Pasos JSON,
    FOREIGN KEY (IdOperacion) REFERENCES Edu_OperacionMatematica(Id)
);

CREATE TABLE IF NOT EXISTS Edu_AvanceCursoJugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    IdCurso CHAR(36) NOT NULL,
    NivelActual INT DEFAULT 1,
    PorcentajeAvance DECIMAL(5,2) DEFAULT 0.0,
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id),
    FOREIGN KEY (IdCurso) REFERENCES Edu_Curso(Id)
);

-- =======================================================
-- 4. EJERCICIOS
-- =======================================================

CREATE TABLE IF NOT EXISTS Edu_Ejercicio (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdCurso CHAR(36) NOT NULL,
    IdTema CHAR(36),
    IdOperacion CHAR(36),
    Enunciado TEXT,
    NivelDificultad INT,
    RespuestaCorrecta TEXT,
    FOREIGN KEY (IdCurso) REFERENCES Edu_Curso(Id),
    FOREIGN KEY (IdTema) REFERENCES Edu_TemaCurso(Id),
    FOREIGN KEY (IdOperacion) REFERENCES Edu_OperacionMatematica(Id)
);

CREATE TABLE IF NOT EXISTS Gam_IntentoEjercicioJugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    IdEjercicio CHAR(36) NOT NULL,
    RespuestaJugador TEXT,
    EsCorrecto BIT,
    PuntosGanados INT,
    FechaIntento BIGINT,
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id),
    FOREIGN KEY (IdEjercicio) REFERENCES Edu_Ejercicio(Id)
);

CREATE TABLE IF NOT EXISTS Gam_HistorialEjerciciosJugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    TotalEjerciciosResueltos INT DEFAULT 0,
    PorcentajeExito DECIMAL(5,2) DEFAULT 0.0,
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id)
);

-- =======================================================
-- 5. COMPETENCIAS
-- =======================================================

CREATE TABLE IF NOT EXISTS Gam_Competencia (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    Tipo VARCHAR(20), -- ARENA, PRACTICA
    Fecha BIGINT,
    DuracionMinutos INT,
    RamasIncluidas JSON,
    ESTADO BIT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Gam_ParticipanteCompetencia (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdCompetencia CHAR(36) NOT NULL,
    IdJugador CHAR(36) NOT NULL,
    PuntosObtenidos INT DEFAULT 0,
    PosicionFinal INT,
    FOREIGN KEY (IdCompetencia) REFERENCES Gam_Competencia(Id),
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id)
);

CREATE TABLE IF NOT EXISTS Gam_HistorialCompetenciasJugador (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador CHAR(36) NOT NULL,
    TotalCompetencias INT DEFAULT 0,
    Victorias INT DEFAULT 0,
    MejorPosicion INT,
    FOREIGN KEY (IdJugador) REFERENCES Seg_Jugador(Id)
);

-- =======================================================
-- SEED DATA
-- =======================================================

-- 1. Persona Admin
INSERT IGNORE INTO Adm_Persona (Id, Nombres, Apellidos, Email, EstudioNivel, ESTADO, FECHA_CREACION) VALUES
('P-ADMIN-001', 'Admin', 'User', 'admin@matharena.com', 'Universidad', 1, 1725375954790);

-- 2. Jugador Admin (Using legacy password 'admin' for simplicity)
INSERT IGNORE INTO Seg_Jugador (Id, IdPersona, Username, PasswordHash, FechaRegistro, EstadoCuenta, ESTADO, FECHA_CREACION) VALUES
('J-ADMIN-001', 'P-ADMIN-001', 'admin', 'admin', 1725375954790, 'ACTIVO', 1, 1725375954790);

-- 3. Cursos
INSERT IGNORE INTO Edu_Curso (Id, Nombre, Descripcion, Rama, Nivel, ESTADO) VALUES
('C-ALG-001', 'Algebra I', 'Fundamentos de algebra', 'Algebra', 'BASICO', 1),
('C-GEO-001', 'Geometria Euclidiana', 'Figuras y Espacio', 'Geometria', 'INTERMEDIO', 1),
('C-CAL-001', 'Calculo Diferencial', 'Limites y Derivadas', 'Calculo', 'AVANZADO', 1);

-- 4. Temporada Actual
INSERT IGNORE INTO Gam_Temporada (Id, Nombre, FechaInicio, FechaFin, ESTADO) VALUES
('S-2025-Q1', 'Temporada 2025-Q1', '2025-01-01', '2025-03-31', 1);

-- 5. Ranking Inicial Admin
INSERT IGNORE INTO Gam_RangoJugadorTemporada (Id, IdJugador, IdTemporada, Rango, PuntosTemporada) VALUES
('R-ADMIN-001', 'J-ADMIN-001', 'S-2025-Q1', 'ORO', 1250);

-- 6. Experiencia Jugador
INSERT IGNORE INTO Gam_ExperienciaJugador (Id, IdJugador, TotalExp) VALUES
('EXP-ADMIN-001', 'J-ADMIN-001', 12450);

-- 7. Racha Jugador
INSERT IGNORE INTO Gam_RachaJugador (Id, IdJugador, RachaActual, RachaMaxima, UltimoIngreso) VALUES
('STR-ADMIN-001', 'J-ADMIN-001', 5, 12, CURDATE());

-- 8. Desafio Diario
INSERT IGNORE INTO Gam_DesafioJugador (Id, IdJugador, FocoPrincipal, Contenido, Estado, FechaAsignacion) VALUES
('CH-ADMIN-001', 'J-ADMIN-001', 'INTEGRAL MASTER', '{"description": "Solve 5 definite integrals perfectly.", "target": 5, "current": 0}', 'PENDIENTE', CURDATE());

-- 9. Avance Curso
INSERT IGNORE INTO Edu_AvanceCursoJugador (Id, IdJugador, IdCurso, NivelActual, PorcentajeAvance) VALUES
('PROG-ADMIN-001', 'J-ADMIN-001', 'C-ALG-001', 5, 75.00);
