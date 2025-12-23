from .base import Entidad

class UsuarioRol(Entidad):
    def __init__(self, Id=None, IdUsuario=None, IdRol=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdUsuario = IdUsuario
        self.IdRol = IdRol
