from .base import Entidad

class Usuario(Entidad):
    def __init__(self, Id=None, NombreUsuario=None, Contrasena=None, IdPersona=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.NombreUsuario = NombreUsuario
        self.Contrasena = Contrasena
        self.IdPersona = IdPersona
    def to_dict(self):
        return {
            'Id': self.Id,
            'NombreUsuario': self.NombreUsuario,
            # 'Contrasena': self.Contrasena, # Security: Don't sending password
            'IdPersona': self.IdPersona,
            'ESTADO': self.ESTADO,
            'RowVersion': self.RowVersion
        }
