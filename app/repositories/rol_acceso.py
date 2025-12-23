from .base import Repository
from entities.rol_acceso import RolAcceso

class RolAccesoRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, RolAcceso, "Seg_Rol_Acceso")
