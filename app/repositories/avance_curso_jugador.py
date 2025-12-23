from .base import Repository
from entities.avance_curso_jugador import AvanceCursoJugador

class AvanceCursoJugadorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, AvanceCursoJugador, "Edu_AvanceCursoJugador")
