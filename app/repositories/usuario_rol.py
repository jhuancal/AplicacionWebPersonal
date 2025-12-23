from .base import Repository
from entities.usuario_rol import UsuarioRol

class UsuarioRolRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, UsuarioRol, "Seg_Usuario_Rol")
