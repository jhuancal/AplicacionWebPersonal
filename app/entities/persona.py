from .base import Entidad

class Persona(Entidad):
    def __init__(self, Id=None, Nombres=None, Apellidos=None, DNI=None, Correo=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Nombres = Nombres
        self.Apellidos = Apellidos
        self.DNI = DNI
        self.Correo = Correo

    def to_dict(self):
        return {
            'Id': self.Id,
            'Nombres': self.Nombres,
            'Apellidos': self.Apellidos,
            'DNI': self.DNI,
            'Correo': self.Correo,
            'ESTADO': self.ESTADO,
            'DISPONIBILIDAD': self.DISPONIBILIDAD,
            'RowVersion': self.RowVersion
        }
