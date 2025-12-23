from .base import Repository
from entities.acceso import Acceso

class AccesoRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Acceso, "Seg_Acceso")
