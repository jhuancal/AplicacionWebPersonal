from .usuario import Usuario

class Cliente(Usuario):
    def __init__(self, NumeroCuenta=None, **kwargs):
        super().__init__(**kwargs)
        self.NumeroCuenta = NumeroCuenta

    def to_dict(self):
        data = super().to_dict()
        data['NumeroCuenta'] = self.NumeroCuenta
        return data
