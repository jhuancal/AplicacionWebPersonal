from db import get_db_connection

sql = """
CREATE TABLE IF NOT EXISTS Gam_MatchPvP (
    Id CHAR(36) NOT NULL PRIMARY KEY,
    IdJugador1 CHAR(36) NOT NULL,
    IdJugador2 CHAR(36), -- Null initially
    Estado VARCHAR(20), -- ESPERANDO, EN_CURSO, FINALIZADO
    PuntuacionJ1 INT DEFAULT 0,
    PuntuacionJ2 INT DEFAULT 0,
    TurnoActual INT DEFAULT 1,
    DatosPartida JSON, -- Stores questions generated for the match
    Ganador CHAR(36),
    FECHA_CREACION BIGINT
);
"""

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    print("Creating Gam_MatchPvP...")
    cursor.execute(sql)
    conn.commit()
    print("Success.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
