from .base import Repository
from entities.operacion_matematica import OperacionMatematica

class OperacionMatematicaRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, OperacionMatematica, "Edu_OperacionMatematica")
