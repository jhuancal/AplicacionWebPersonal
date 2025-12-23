from .base import Repository
from entities.puntaje_jugador import PuntajeJugador

class PuntajeJugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, PuntajeJugador, "Gam_PuntajeJugador")
