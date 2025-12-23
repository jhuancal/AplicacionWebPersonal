from .base import Entidad

class Ejercicio(Entidad):
    def __init__(self, Id=None, IdCurso=None, IdTema=None, IdOperacion=None, Enunciado=None, NivelDificultad=None, RespuestaCorrecta=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.IdCurso = IdCurso
        self.IdTema = IdTema
        self.IdOperacion = IdOperacion
        self.Enunciado = Enunciado
        self.NivelDificultad = NivelDificultad
        self.RespuestaCorrecta = RespuestaCorrecta

    def to_dict(self):
        return {
            'Id': self.Id,
            'IdCurso': self.IdCurso,
            'IdTema': self.IdTema,
            'IdOperacion': self.IdOperacion,
            'Enunciado': self.Enunciado,
            'NivelDificultad': self.NivelDificultad,
            'RespuestaCorrecta': self.RespuestaCorrecta
        }
