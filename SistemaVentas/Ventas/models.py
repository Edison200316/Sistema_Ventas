from django.db import models
from decimal import Decimal

# BaseModel definition with the corrected Meta placement
class BaseModel(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Ensure this is inside the class

# Producto model
class Producto(BaseModel):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Producto: {self.nombre}(${self.precio})'

# Cliente model
class Cliente(BaseModel):
    cedula = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=225)

    def __str__(self):
        return f'Cliente: {self.nombre} {self.apellido} - Cedula : {self.cedula}'

# Orden model
class Orden(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_totales(self):
        self.subtotal = sum(producto.precio for producto in self.productos.all())
        self.iva = self.subtotal * Decimal('0.15')
        self.total = self.subtotal + self.iva
        self.save()

    def __str__(self):
        return f'Orden: {self.id} - Cliente:{self.cliente.nombre} - Total: ${self.total}'

         
