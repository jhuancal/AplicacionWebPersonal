from .base import Repository
from entities.curso import Curso

class CursoRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Curso, "Edu_Curso")
