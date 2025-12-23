from .base import Repository
from entities.experiencia_jugador import ExperienciaJugador

class ExperienciaJugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, ExperienciaJugador, "Gam_ExperienciaJugador")
