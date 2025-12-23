class Entidad:
    def __init__(self, USER_CREACION=None, USER_MODIFICACION=None,
                 FECHA_CREACION=None, FECHA_MODIFICACION=None, ESTADO=None, DISPONIBILIDAD=None, RowVersion=None, **kwargs):
        self.USER_CREACION = USER_CREACION
        self.USER_MODIFICACION = USER_MODIFICACION
        self.FECHA_CREACION = FECHA_CREACION
        self.FECHA_MODIFICACION = FECHA_MODIFICACION
        self.ESTADO = ESTADO
        self.DISPONIBILIDAD = DISPONIBILIDAD
        self.RowVersion = RowVersion
