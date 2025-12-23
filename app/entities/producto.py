from .base import Entidad

class Producto(Entidad):
    def __init__(self, Id=None, Nombre=None, Descripcion=None, PrecioRegular=None, 
                 PrecioVenta=None, Descuento=None, DiaLlegada=None, UrlImagen=None, **kwargs):
        super().__init__(**kwargs)
        self.Id = Id
        self.Nombre = Nombre
        self.Descripcion = Descripcion
        self.PrecioRegular = PrecioRegular
        self.PrecioVenta = PrecioVenta
        self.Descuento = Descuento
        self.DiaLlegada = DiaLlegada
        self.UrlImagen = UrlImagen

    def to_dict(self):
        return {
            'Id': self.Id,
            'Nombre': self.Nombre,
            'Descripcion': self.Descripcion,
            'PrecioRegular': self.PrecioRegular,
            'PrecioVenta': self.PrecioVenta,
            'Descuento': self.Descuento,
            'DiaLlegada': self.DiaLlegada,
            'UrlImagen': self.UrlImagen,
            'ESTADO': self.ESTADO,
            'DISPONIBILIDAD': self.DISPONIBILIDAD,
            'USER_CREACION': self.USER_CREACION
            # Add other fields if needed, primarily for JSON serialization
        }
