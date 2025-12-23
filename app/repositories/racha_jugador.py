from .base import Repository
from entities.racha_jugador import RachaJugador

class RachaJugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, RachaJugador, "Gam_RachaJugador")
