from .base import Repository
from entities.metodo_resolucion import MetodoResolucion

class MetodoResolucionRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, MetodoResolucion, "Edu_MetodoResolucion")
