from .base import Repository
from entities.recurso_curso import RecursoCurso

class RecursoCursoRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, RecursoCurso, "Edu_RecursoCurso")
