from .base import Repository
from entities.examen_curso import ExamenCurso

class ExamenCursoRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, ExamenCurso, "Edu_ExamenCurso")
