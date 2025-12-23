from .base import Repository
from entities.tema_curso import TemaCurso

class TemaCursoRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, TemaCurso, "Edu_TemaCurso")
