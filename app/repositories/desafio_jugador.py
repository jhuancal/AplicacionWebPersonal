from .base import Repository
from entities.desafio_jugador import DesafioJugador

class DesafioJugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, DesafioJugador, "Gam_DesafioJugador")
