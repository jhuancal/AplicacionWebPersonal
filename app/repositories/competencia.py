from .base import Repository
from entities.competencia import Competencia

class CompetenciaRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Competencia, "Gam_Competencia")
