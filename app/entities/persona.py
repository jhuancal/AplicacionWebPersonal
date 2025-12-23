from .base import Entidad

class Persona(Entidad):
    def __init__(self, Id=None, Nombres=None, Apellidos=None, Dni=None, FechaNacimiento=None, Email=None, EstudioNivel=None, Institucion=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Nombres = Nombres
        self.Apellidos = Apellidos
        self.Dni = Dni        
        self.FechaNacimiento = FechaNacimiento
        self.Email = Email
        self.EstudioNivel = EstudioNivel
        self.Institucion = Institucion

    def to_dict(self):
        return {
            'Id': self.Id,
            'Nombres': self.Nombres,
            'Apellidos': self.Apellidos,
            'DNI': self.Dni,
            'FechaNacimiento': self.FechaNacimiento,
            'Email': self.Email,
            'EstudioNivel': self.EstudioNivel,
            'Institucion': self.Institucion,
            'ESTADO': self.ESTADO
        }
