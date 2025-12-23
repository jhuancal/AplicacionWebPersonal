from .base import Entidad

class Jugador(Entidad):
    def __init__(self, Id=None, Username=None, PasswordHash=None, IdPersona=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Username = Username
        self.PasswordHash = PasswordHash
        self.IdPersona = IdPersona

    def to_dict(self):
        return {
            'Id': self.Id,
            'Username': self.Username,
            # 'PasswordHash': self.PasswordHash, # Security
            'IdPersona': self.IdPersona,
            'ESTADO': self.ESTADO
        }
