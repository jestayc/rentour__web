from django.db import models
from django import forms
from django.contrib.auth.models import User
from enum import Enum
import datetime
from django.utils import timezone
from users.models import Usuario

# Create your models here.


class Departamento(models.Model):

    id_depto = models.AutoField(primary_key=True, editable=False)
    referencia = models.CharField( blank = False, null = False, max_length=100, verbose_name='Referencia')
    direccion = models.CharField( blank = False, null = False, max_length=256, verbose_name='Dirección')
    zona = models.CharField( blank = False, null = False, max_length=100, verbose_name='Zona')
    valor_arriendo = models.IntegerField( blank = False, null = False, verbose_name='Valor Arriendo')
    pct_anticipo = models.IntegerField('Porcentaje de Anticipo', blank=False, null=False, default=50)
    dormitorio = models.IntegerField( blank = False, null = False, verbose_name='Número de dormitorios')
    baño = models.IntegerField( blank = False, null = False, verbose_name='Cantidad baños')
    detalles = models.TextField( blank = True, null = True, verbose_name='Información Adicional')
    image = models.CharField( blank = False, null = True, max_length=500, verbose_name='Imagen')

    class ESTADO_DEPTO(Enum):
        
        disponible = ('Disponible', 'Disponible')
        mantencion = ('Mantencion', 'Mantencion')
        nuevo      = ('Nuevo', 'Nuevo')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    estado_depto = models.CharField(
        max_length=100,
        choices=[x.value for x in ESTADO_DEPTO]
    )   


    class Meta:
        ordering = ['referencia']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.referencia
        

class TipoServicioExtra(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_servicio = models.CharField( max_length=50, blank=False, null=False, verbose_name="Tipo Servicio Extra")
    descripcion = models.TextField( blank=False, null=False, verbose_name='Descripción')

    class Meta:
        ordering = ['id']
        verbose_name = 'Tipo Servicio Extra'
        verbose_name_plural = 'Tipos Servicios Extras'
    
    def __str__(self):
        return self.tipo_servicio


class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_depto = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    n_personas = models.IntegerField('Número Visitantes', blank=False, null=False, default=0)
    n_dias = models.IntegerField('Cantidad de Días', blank=False, null=False, default=0)
    visitantes = models.TextField( blank=False, null=False, verbose_name='Visitantes',default='' )

    
    pago_anticipo = models.IntegerField('Pago Anticipo', blank=False, null=False, default=0)
    pago_faltante = models.IntegerField('Pago Faltante', blank=False, null=False, default=0)
    pago_multa = models.IntegerField('Pago Multa', blank=False, null=False, default=0)
    pago_servicioextra = models.IntegerField('Pago Servicio Extra', blank=False, null=False, default=0)
    pago_total = models.IntegerField('Pago Total', blank=False, null=False, default=0)
    
    monto_estadia = models.IntegerField('Monto Estadía', blank=False, null=False, default=0)
    monto_pordia = models.IntegerField('Monto por Día', blank=False, null=False, default=0)
    monto_servicioextra = models.IntegerField('Monto Servicios Extras', blank=False, null=False, default=0)
    monto_multa = models.IntegerField('Monto Multas', blank=False, null=False, default=0)
    monto_total = models.IntegerField('Monto Total', blank=False, null=False, default=0)

    fecha_reserva = models.DateField('Fecha Reserva', blank=False, null=False, auto_now=False, auto_now_add=False, default=datetime.date.today, editable = False)
    fecha_inicio = models.DateField('Fecha Inicio', blank=False, null=False, auto_now=False, auto_now_add=False, default=datetime.date.today)
    fecha_termino = models.DateField('Fecha Termino', blank=False, null=False, auto_now=False, auto_now_add=False, default=datetime.date.today)
    
    def por_pagar_estadia(self):
        return self.monto_estadia - self.pago_anticipo - self.pago_faltante



    class ESTADO_RESERVA(Enum):
        solicitud = ('Solicitud', 'Solicitud') #Probando el Sistema
        nueva = ('Nueva', 'Nueva') #Confirmada y pagada el porcentaje de Reserva
        enuso = ('En uso', 'En uso') #En uso llego el cliente
        anulada = ('Anulada', 'Anulada') #Anular la Reserva por diferentes motivos (Mantención, No Pago, Siniestro)
        reembolso = ('Reembolsado', 'Reembolsado')# Reembolso de la reserva
        finalizada = ('Finalizada', 'Finalizada') #Terminó con CheckOut

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    estado_reserva = models.CharField(
        max_length=100,
        choices=[x.value for x in ESTADO_RESERVA]
    ) 
    class Meta:
        ordering = ['-id']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

  
    def __str__(self):
        return 'Reserva ' + str(self.id) + ' - ' + self.id_usuario.nombres + ' - ' + self.id_depto.referencia

def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class DetalleServicio(models.Model):
    id = models.AutoField(primary_key=True)
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    id_depto = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    id_tiposervicioextra = models.ForeignKey(TipoServicioExtra, on_delete=models.CASCADE)

    check_pago = models.BooleanField('Completó Pago', blank=False, null=False, default=False)

    conductor = models.CharField( max_length=100, blank=True, null=True, verbose_name="Nombre Conductor")
    ubicacion = models.CharField( max_length=100, blank=True, null=True, verbose_name="Ubicación")
    vehiculo = models.CharField( max_length=10, blank=True, null=True, verbose_name="Patente")
    valor = models.IntegerField('Valor', blank=True, null=True, default=0)
    fecha_dia = models.DateField('Fecha', auto_now_add=False, blank=False, default = timezone.now)
    fecha_hora = models.TimeField('Hora', auto_now_add=False, blank=False, default = timezone.now )

    class ESTADO_SERVICIO(Enum):
            solicitud = ('Solicitud', 'Solicitud')
            aceptada = ('Aceptada', 'Aceptada')
            pagado = ('Pagado', 'Pagado')
            anulada = ('Anulada', 'Anulada')
            realizado = ('Realizado', 'Realizado')

            @classmethod
            def get_value(cls, member):
                return cls[member].value[0]

    estado_servicio = models.CharField(
            max_length=100,
            choices=[x.value for x in ESTADO_SERVICIO]
        ) 

    def __str__(self):
        return str(self.id_reserva) + ' - ' + str(self.id_tiposervicioextra)

class RecibirPago(models.Model):
    id = models.AutoField(primary_key=True)
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    id_detalleservicio = models.ForeignKey(DetalleServicio, on_delete=models.CASCADE, blank=True, null = True)
    monto = models.IntegerField('Monto', blank=False, null=False, default=0)
    observaciones = models.CharField( max_length=100, blank=False, null=True, verbose_name="Observaciones")
    fecha = models.DateTimeField('Fecha', blank=False, null=False, default = timezone.now)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Recibir Pago'
        verbose_name_plural = 'Recibir Pagos'

    def __str__(self):
        return str(self.id) 

class Elemento(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField( max_length=100, blank=False, null=False, verbose_name="Nombre Articulo")
    valor = models.IntegerField('Valor', blank=False, null=False, default=0)


    class Meta:
        ordering = ['nombre']
        verbose_name = 'Elemento'
        verbose_name_plural = 'Elementos'

    def __str__(self):
        return str(self.nombre) + ' - ' + str(self.valor)



class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    id_depto = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    id_elemento = models.ForeignKey(Elemento, on_delete=models.CASCADE)
    cantidad = models.IntegerField('Cantidad', blank=False, null=False, default=0)
    
    def __str__(self):
        return str(self.id_depto) + ' - ' + str(self.id_elemento) + ' - ' + str(self.cantidad) 

class TipoMantencion(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_servicio = models.CharField( max_length=50, blank=False, null=False, verbose_name="Tipo de Mantención")
    descripcion = models.TextField( blank=False, null=False, verbose_name='Descripción')

    class Meta:
        ordering = ['id']
        verbose_name = 'Tipo de Mantención'
        verbose_name_plural = 'Tipos de Mantenciones'

    def __str__(self):
        return str(self.tipo_servicio) 

class Mantencion(models.Model):
    id = models.AutoField(primary_key=True) 
    id_mantencion = models.ForeignKey(TipoMantencion, on_delete=models.CASCADE) 
    id_depto = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    costo_mantencion = models.IntegerField('Costo Mantención', blank=False, null=False, default=0)

    fecha_creacion = models.DateField('Fecha Creación', blank=False, null=False, auto_now=False, auto_now_add=False, default=datetime.date.today, editable = False)
    fecha_inicio = models.DateField('Fecha Inicio', blank=False, null=False, auto_now=False, auto_now_add=False, default=datetime.date.today)
    fecha_termino = models.DateField('Fecha Termino', blank=False, null=False, auto_now=False, auto_now_add=False, default=datetime.date.today)

    class ESTADO_MANTENCION(Enum):
        nueva = ('Nueva', 'Nueva')
        realizado = ('Realizado', 'Realizado')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    estado_mantencion = models.CharField(
            max_length=100,
            choices=[x.value for x in ESTADO_MANTENCION],default='Nueva'
        ) 

    class Meta:
        ordering = ['-id']
        verbose_name = 'Mantención'
        verbose_name_plural = 'Mantenciones'

    def __str__(self):
        return 'Mantención' + ' - ' + str(self.id_depto) + ' - ' + str(self.fecha_inicio)+ ' - ' + str(self.fecha_termino)

class Agenda(models.Model):
    id = models.AutoField(primary_key=True) 
    id_depto = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, blank=True, null = True)
    id_mantencion = models.ForeignKey(Mantencion, on_delete=models.CASCADE, blank=True, null= True)
    fecha_inicio = models.DateField('Fecha Inicio', blank=False, null=False, auto_now=False, auto_now_add=False, default=datetime.date.today)
    fecha_termino = models.DateField('Fecha Termino', blank=False, null=False, auto_now=False, auto_now_add=False, default=datetime.date.today)

    class Meta:
        ordering = ['id']
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'

    def __str__(self):
        return str(self.id_depto) + ' - ' + str(self.id_reserva)+ ' - ' + str(self.id_mantencion)
  
class CheckList(models.Model):
    id = models.AutoField(primary_key=True)  
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)

    id_inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    check = models.BooleanField(blank=False, null=False, default=True)
    cantidad_real = models.IntegerField('Cantidad Real', blank=False, null=False, default=0)
    monto_multa = models.IntegerField('Monto Multa', blank=False, null=False, default=0)
   
    class Meta:
        ordering = ['id']
        verbose_name = 'CheckList'
        verbose_name_plural = 'Checks List'

    def __str__(self):
        return str(self.id_reserva) + ' - ' + str(self.id_inventario) 

class CheckIn(models.Model):

 
    id_reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, primary_key=True)
   
    check_pago = models.BooleanField('Completó Pago', blank=False, null=False, default=False)
    check_lista = models.BooleanField('CheckList Realizado', blank=False, null=False, default=False)
    check_pdf = models.BooleanField('Impresión PDF', blank=False, null=False, default=False)
    check_servicio = models.BooleanField('Servicios Extras', blank=False, null=False, default=False)
    check_llave = models.BooleanField('Entrega Llave', blank=False, null=False, default=False)

    class Meta:
        ordering = ['id_reserva']
        verbose_name = 'CheckIn'
        verbose_name_plural = 'Checks In'
   
    def __str__(self):
        return str(self.id_reserva)


class CheckOut(models.Model):
    id_reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, primary_key=True)
    check_lista = models.BooleanField('CheckList Realizado', blank=False, null=False, default=False)
    detalle_multa = models.TextField( blank=False, null=False, verbose_name='Detalle Multa', default='' )
    check_multa = models.BooleanField('Cálculo Multa', blank=False, null=False, default=False)
    total_multa = models.IntegerField('Monto Multa', blank=False, null=False, default=0)
    check_pdf = models.BooleanField('Impresión PDF', blank=False, null=False, default=False)
    
   
    class Meta:
        ordering = ['id_reserva']
        verbose_name = 'CheckOut'
        verbose_name_plural = 'Checks Out'

    def __str__(self):
        return str(self.id_reserva) 
