from .usuario import Usuario

class Colaborador(Usuario):
    def __init__(self, IdRol=None, EsActivo=None, FechaContratacion=None, **kwargs):
        super().__init__(**kwargs)
        self.IdRol = IdRol
        self.EsActivo = EsActivo
        self.FechaContratacion = FechaContratacion

    def to_dict(self):
        data = super().to_dict()
        data['IdRol'] = self.IdRol
        data['EsActivo'] = self.EsActivo
        data['FechaContratacion'] = self.FechaContratacion
        return data
