class Entidad:
    def __init__(self, USER_CREACION=None, FECHA_CREACION=None, ESTADO=None, RowVersion=None, **kwargs):
        self.USER_CREACION = USER_CREACION
        self.FECHA_CREACION = FECHA_CREACION
        self.ESTADO = ESTADO
        self.RowVersion = RowVersion
