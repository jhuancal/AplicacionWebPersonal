from .base import Repository
from entities.historial_competencias_jugador import HistorialCompetenciasJugador

class HistorialCompetenciasJugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, HistorialCompetenciasJugador, "Gam_HistorialCompetenciasJugador")
