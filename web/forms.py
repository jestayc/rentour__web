from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, CreateView,  UpdateView, FormView, ListView, RedirectView
from django import forms
from .models import *
from .widgets import BootstrapDateTimePickerInput

class lista_ver(LoginRequiredMixin, ListView):
    model = Reserva
    paginate_by = 8
    template_name = 'lista.html'
    queryset = Reserva.objects.all()
    context_object_name = 'items'



class DepartamentoFormNew(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ('referencia','direccion','zona','valor_arriendo','pct_anticipo','dormitorio','baño','detalles','image')

        labels = {
            'referencia':'Referencia',
            'direccion':'Direccion',
            'zona':'Zona',
            'valor_arriendo':'Valor Arriendo',
            'pct_anticipo':'Porcentaje Anticipo',
            'dormitorio':'Dormitorios',    
            'baño':'Baños',    
            'detalles':'Detalles',              
            'image':'Imagen'
            }
        widgets= {
            'referencia': forms.TextInput(attrs={'class':'form-control','id':'referencia'}),
            'direccion': forms.TextInput(attrs={'class':'form-control','id':'direccion'}),
            'zona': forms.TextInput(attrs={'class':'form-control','id':'zona'}),
            'valor_arriendo':forms.TextInput(attrs={'class':'form-control','id':'valor_arriendo'}),
        	'pct_anticipo': forms.TextInput(attrs={'class':'form-control','id':'pct_anticipo'}),
            'dormitorio': forms.TextInput(attrs={'class':'form-control','id':'dormitorio'}),
            'baño':forms.TextInput(attrs={'class':'form-control','id':'baño'}),
        	'detalles': forms.TextInput(attrs={'class':'form-control','id':'detalles'}),
            'image': forms.TextInput(attrs={'class':'form-control','id':'image'}),

        }

class DepartamentoFormEdit(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ('referencia','image','direccion','zona','valor_arriendo','pct_anticipo','dormitorio','baño','detalles', 'estado_depto')

        labels = {
            'referencia':'Referencia',                         
            'image':'Imagen',
            'direccion':'Direccion',
            'zona':'Zona',
            'valor_arriendo':'Valor Arriendo',
            'pct_anticipo':'Porcentaje Anticipo',
            'dormitorio':'Dormitorios',    
            'baño':'Baños',    
            'detalles':'Detalles',              
            'estado_depto': 'Estado Departamento'
            }
        widgets= {
            'referencia': forms.TextInput(attrs={'class':'form-control','id':'referencia','readonly':True}),
            
            'image': forms.TextInput(attrs={'class':'form-control','id':'image'}),
            'direccion': forms.TextInput(attrs={'class':'form-control','id':'direccion','readonly':True}),
            'zona': forms.TextInput(attrs={'class':'form-control','id':'zona','readonly':True}),
            'valor_arriendo':forms.TextInput(attrs={'class':'form-control','id':'valor_arriendo'}),
        	'pct_anticipo': forms.TextInput(attrs={'class':'form-control','id':'pct_anticipo'}),
            'dormitorio': forms.TextInput(attrs={'class':'form-control','id':'dormitorio'}),
            'baño':forms.TextInput(attrs={'class':'form-control','id':'baño'}),
        	'detalles': forms.TextInput(attrs={'class':'form-control','id':'detalles'}),
            'estado_depto': forms.Select(attrs={'class': 'form-control','id': 'estado_depto'}),
        }


class DepartamentoDisponibilidadFormEdit(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ('referencia','direccion','zona','valor_arriendo','pct_anticipo','dormitorio','baño','detalles', 'estado_depto')

        labels = {
            'referencia':'Referencia',
            'direccion':'Direccion',
            'zona':'Zona',
            'valor_arriendo':'Valor Arriendo',
            'pct_anticipo':'Porcentaje Anticipo',
            'dormitorio':'Dormitorios',    
            'baño':'Baños',    
            'detalles':'Detalles',              
            'estado_depto': 'Estado Departamento'
            }
        widgets= {
            'referencia': forms.TextInput(attrs={'class':'form-control','id':'referencia','readonly':True}),
            'direccion': forms.TextInput(attrs={'class':'form-control','id':'direccion','readonly':True}),
            'zona': forms.TextInput(attrs={'class':'form-control','id':'zona','readonly':True}),
            'valor_arriendo':forms.TextInput(attrs={'class':'form-control','id':'valor_arriendo','readonly':True}),
        	'pct_anticipo': forms.TextInput(attrs={'class':'form-control','id':'pct_anticipo','readonly':True}),
            'dormitorio': forms.TextInput(attrs={'class':'form-control','id':'dormitorio','readonly':True}),
            'baño':forms.TextInput(attrs={'class':'form-control','id':'baño','readonly':True}),
        	'detalles': forms.TextInput(attrs={'class':'form-control','id':'detalles','readonly':True}),
            'estado_depto': forms.Select(attrs={'class': 'form-control','id': 'estado_depto'}),
        }


class TipoMantencionFormNew(forms.ModelForm):
    class Meta:
        model = TipoMantencion
        fields = ('tipo_servicio','descripcion',)

        labels = {
            'tipo_servicio':'Tipo de Servicio',
            'descripcion':'Descripción del servicio',
            }
        widgets= {
            'tipo_servicio': forms.TextInput(attrs={'class':'form-control','id':'tipo_servicio'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control','id':'descripcion'}),
        }

class MantencionFormNew(forms.ModelForm):
    class Meta:
        model = Mantencion
        fields = ('id_mantencion', 'costo_mantencion', 'fecha_inicio', 'fecha_termino')

        labels = {
            'id_mantencion':'Tipo Mantención',
            'costo_mantencion':'Costo Mantención',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_termino': 'Fecha de Término'
            }
        widgets= {  
            'id_mantencion': forms.Select(attrs={'class':'form-control','id':'id_mantencion'}),        
            'costo_mantencion': forms.TextInput(attrs={'class':'form-control','id':'costo_mantencion'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
        }


class TipoServicioExtraFormNew(forms.ModelForm):
    class Meta:
        model = TipoServicioExtra
        fields = ('tipo_servicio','descripcion')

        labels = {
            'tipo_servicio':'Tipo de Servicio',
            'descripcion':'Descripción',
            }
        widgets= {
            'tipo_servicio': forms.TextInput(attrs={'class':'form-control','id':'tipo_servicio'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control','id':'descripcion'}),
        }

class DetalleServicioFormEdit(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ('id_reserva','id_depto', 'id_tiposervicioextra','conductor', 'ubicacion','vehiculo', 'valor', 'fecha_dia', 'estado_servicio')

        labels = {
            'id_reserva':'Reserva',
            'id_depto':'Departamento',
            'id_tiposervicioextra':'Tipo de Servicio',
            'conductor':'Conductor',
            'ubicacion':'Ubicación',
            'vehiculo':'Vehículo',
            'valor':'Valor',
            'fecha_dia':'Fecha Dia',
            'estado_servicio':'Estado de Servicio',
            }
        widgets= {
            'id_reserva': forms.Select(attrs={'class':'form-control','id':'id_reserva'}),
            'id_depto': forms.Select(attrs={'class':'form-control','id':'id_depto'}),
            'id_tiposervicioextra': forms.Select(attrs={'class':'form-control','id':'id_tiposervicioextra'}),
            'conductor': forms.TextInput(attrs={'class':'form-control','id':'conductor'}),
            'ubicacion': forms.TextInput(attrs={'class':'form-control','id':'ubicacion'}),
            'vehiculo': forms.TextInput(attrs={'class':'form-control','id':'vehiculo'}),
            'valor': forms.TextInput(attrs={'class':'form-control','id':'valor'}),
            'fecha_dia': forms.DateInput(attrs={'type': 'date'}),
            'estado_servicio': forms.Select(attrs={'class':'form-control','id':'estado_servicio'}),
        }

class ElementoFormNew(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ('nombre','valor',)

        labels = {
            'nombre':'Nombre del Elemento',
            'valor':'Valor del Elemento',
            }
        widgets= {
            'nombre': forms.TextInput(attrs={'class':'form-control','id':'nombre'}),
            'valor': forms.TextInput(attrs={'class':'form-control','id':'valor'}),
        }

class InventarioFormNew(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ('id_elemento', 'cantidad')

        labels = {
            'id_elemento':'Artículo',
            'cantidad':'Cantidad',
            }
        widgets= {  
            'id_elemento': forms.Select(attrs={'class':'form-control','id':'id_elemento'}),        
            'cantidad': forms.TextInput(attrs={'class':'form-control','id':'cantidad'}),
        }

class EditarMantencion(forms.ModelForm):
    class Meta:
        model = Mantencion
        fields = ( 'id_mantencion','estado_mantencion','costo_mantencion',  'fecha_inicio', 'fecha_termino' )

        labels = {
            'id_mantencion':'Tipo Mantención',
            'estado_mantencion': 'Estado Mantención',
            'costo_mantencion':'Costo Mantención',
            'fecha_inicio' : 'Fecha Inicio',
            'fecha_termino':'Fecha Término'
            
            }
        widgets= {  
            'id_mantencion': forms.Select(attrs={'class':'form-control','id':'id_mantencion'}), 
            'estado_mantencion': forms.Select(attrs={'class':'form-control','id':'estado_mantencion'}),      
            'costo_mantencion': forms.TextInput(attrs={'class':'form-control','id':'costo_mantencion'}),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','id':'fecha_inicio','type': 'date'}),
            'fecha_termino': forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','id':'fecha_termino','type': 'date'}),
        }

class CheckInFormNew(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ( 'check_pdf', 'check_lista', 'check_pago', 'check_servicio', 'check_llave')

        labels = {
         
            'check_pdf':'Entrega de PDF',
            'check_lista': 'Check de Inventario',
            'check_pago': 'Check de Pago',
            'check_servicio': 'Check Servicio Extra',
            'check_llave': 'Entrega llaves'
            }
        widgets= {  
                 
            'check_pdf': forms.CheckboxInput(attrs={'class':'form-control','id':'check_pdf'}),
            'check_lista': forms.CheckboxInput(attrs={'class':'form-control','id':'check_lista'}),
            'check_pago': forms.CheckboxInput(attrs={'class':'form-control','id':'check_pago'}),
            'check_servicio': forms.CheckboxInput(attrs={'class':'form-control','id':'check_servicio'}),
            'check_llave': forms.CheckboxInput(attrs={'class':'form-control','id':'check_llave'}),
        }

class CheckListFormNew(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = ('id_inventario', 'check', 'cantidad_real', 'monto_multa')

        labels = {
            'id_inventario':'Inventario',
            'check': 'Check',
            'cantidad_real': 'Cantidad Real',
            'monto_multa': 'Monto de Multa',
            }
        widgets= {  
            'id_inventario': forms.Select(attrs={'class':'form-control','id':'id_inventario'}),
            'check': forms.CheckboxInput(attrs={'class':'form-control','id':'check'}),
            'cantidad_real': forms.TextInput(attrs={'class':'form-control','id':'cantidad_real'}),
            'monto_multa': forms.TextInput(attrs={'class':'form-control','id':'monto_multa'}),
        }


class CheckListFormEdit(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = ('cantidad_real',)
        labels = {
            'cantidad_real': 'Cantidad Real',
            }
        widgets= {  
            'cantidad_real': forms.TextInput(attrs={'class':'form-control','id':'cantidad_real'}),
        }

class CheckOutFormNew(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ( 'check_lista', 'detalle_multa', 'check_multa', 'total_multa', 'check_pdf')

        labels = {
            
            'check_lista':'Revisa Inventario',
            'detalle_multa': 'Detalle de Multa',
            'check_multa': 'Check Multa',
            'total_multa': 'Total Multa',
            'check_pdf': 'Entrega de PDF',
            }
        widgets= {  
            
            'check_lista': forms.CheckboxInput(attrs={'class':'form-control','id':'check_lista'}),
            'detalle_multa': forms.TextInput(attrs={'class':'form-control','id':'detalle_multa'}),
            'check_multa': forms.CheckboxInput(attrs={'class':'form-control','id':'check_multa'}),
            'total_multa': forms.TextInput(attrs={'class':'form-control','id':'total_multa'}),
            'check_pdf': forms.CheckboxInput(attrs={'class':'form-control','id':'check_pdf'}),
        }


class ReservaFormNew(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('id_usuario','n_personas', 'n_dias', 'visitantes', 'pago_anticipo', 'pago_faltante', 'pago_multa', 
                   'pago_servicioextra', 'pago_total', 'monto_estadia', 'monto_pordia', 'monto_servicioextra', 
                   'monto_multa', 'monto_total', 'fecha_inicio', 'fecha_termino')

        labels = {
            'id_usuario':'Usuario',
            'n_personas':'Numero de personas',
            'n_dias':'Numero de días',
            'visitantes': 'Visitantes',
            'pago_anticipo': 'Pago Anticipado',
            'pago_faltante': 'Pago Faltante',
            'pago_multa': 'Pago Multa',

            'pago_servicioextra':'Pago Servicio Extra',
            'pago_total':'Pago Total',
            'monto_estadia': 'Monto Estadía',
            'monto_pordia': 'Monto por día',
            'monto_servicioextra': 'Monto Servicio Extra',
            'monto_multa': 'Monto Multa',
            'monto_total': 'Monto Total',
            'fecha_inicio': 'Fecha Inicio',
            'fecha_termino': 'Fecha Término'
            }
        widgets= {
             'id_usuario': forms.Select(attrs={'class':'form-control','id':'id_usuario'}),        
            'n_personas': forms.TextInput(attrs={'class':'form-control','id':'n_personas'}),        
            'n_dias': forms.TextInput(attrs={'class':'form-control','id':'n_dias'}),
            'visitantes': forms.TextInput(attrs={'class':'form-control','id':'visitantes'}),
            'pago_anticipo': forms.TextInput(attrs={'class':'form-control','id':'pago_anticipo'}),
            'pago_faltante': forms.TextInput(attrs={'class':'form-control','id':'pago_faltante'}),
            'pago_multa': forms.TextInput(attrs={'class':'form-control','id':'pago_multa'}),

            'pago_servicioextra': forms.TextInput(attrs={'class':'form-control','id':'pago_servicioextra'}),        
            'pago_total': forms.TextInput(attrs={'class':'form-control','id':'pago_total'}),
            'monto_estadia': forms.TextInput(attrs={'class':'form-control','id':'monto_estadia'}),
            'monto_pordia': forms.TextInput(attrs={'class':'form-control','id':'monto_pordia'}),
            'monto_servicioextra': forms.TextInput(attrs={'class':'form-control','id':'monto_servicioextra'}),
            'monto_multa': forms.TextInput(attrs={'class':'form-control','id':'monto_multa'}),
            'monto_total': forms.TextInput(attrs={'class':'form-control','id':'monto_total'}),

            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
        }

class ReservaInicialPaso1(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('n_personas', 'visitantes','fecha_inicio', 'n_dias')

        labels = {
            'n_personas':'Cantidad de Visitantes',
            'visitantes': 'Visitantes',
            'fecha_inicio': 'Fecha Inicio',
            'n_dias' : 'Estadía en Días'
            }
        widgets= {      
            'n_personas': forms.TextInput(attrs={'class':'form-control','id':'n_personas'}),        
            'visitantes': forms.TextInput(attrs={'class':'form-control','id':'visitantes'}),
            'fecha_inicio': forms.DateInput(attrs={'class':'form-control','id':'fecha_inicio','type': 'date'}),
            'n_dias': forms.TextInput(attrs={'class':'form-control','id':'n_dias'}),

        }

class ReservaInicialPaso2(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('visitantes', 'n_personas')

        labels = {
            'visitantes':'Visitantes',
            'n_personas': 'n_personas'

            }
        widgets= {      
            'visitantes': forms.TextInput(attrs={'class':'form-control','id':'visitantes'}),   
            'n_personas': forms.TextInput(attrs={'class':'form-control','id':'n_personas'})             

        }

class DetalleServicioFormNew(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ('id_reserva', 'id_tiposervicioextra', 'ubicacion',  'fecha_dia',  'fecha_hora', 'conductor', 
        'ubicacion', 'vehiculo', 'valor', 'estado_servicio')

        labels = {
            'id_reserva':'Reserva',
            'id_tiposervicioextra':'Tipo de Servicio Extra',
            'ubicacion': 'Ubicación',
            'fecha_dia':'Fecha de Realización',
            'fecha_hora':'Hora de Realización',
            'conductor': 'Conductor',
            'vehiculo': 'Vehiculo',
            'valor': 'Valor',
            'estado_servicio':'Estado de Servicio',

            }
        widgets= {
            'id_reserva': forms.Select(attrs={'class':'form-control','id':'id_tiposervicioextra'}),        
            'id_tiposervicioextra': forms.Select(attrs={'class':'form-control','id':'id_tiposervicioextra'}),
            'ubicacion': forms.TextInput(attrs={'class':'form-control','id':'ubicacion'}),
            'fecha_dia': forms.DateInput(attrs={'class':'form-control','id':'fecha_dia','type': 'date'}),
            'fecha_hora': forms.TimeInput(format='%H:%M',attrs={'class':'form-control','id':'fecha_hora','type': 'time'}),
            'conductor': forms.TextInput(attrs={'class':'form-control','id':'conductor'}),
            'vehiculo': forms.TextInput(attrs={'class':'form-control','id':'vehiculo'}),
            'valor': forms.TextInput(attrs={'class':'form-control','id':'valor'}),
            'estado_servicio': forms.Select(attrs={'class':'form-control','id':'estado_servicio'}),

        }

class DetalleServicios(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ('id_tiposervicioextra',)

        labels = {

            'id_tiposervicioextra':'Tipo de Servicio Extra',

            }
        widgets= {
      
            'id_tiposervicioextra': forms.TextInput(attrs={'class':'form-control','id':'id_tiposervicioextra'}),
     
        }

class RecibirPagoFormNew(forms.ModelForm):
    class Meta:
        model = RecibirPago
        fields = ('id_reserva', 'monto', 'observaciones')

        labels = {

            'id_reserva':'Reserva',
            'monto':'Monto',
            'observaciones': 'Observaciones'

            }
        widgets= {
      
            'id_reserva': forms.TextInput(attrs={'class':'form-control','id':'id_reserva','readonly':True}),
            'monto': forms.TextInput(attrs={'class':'form-control','id':'monto','readonly':True}),
            'observaciones': forms.TextInput(attrs={'class':'form-control','id':'observaciones','readonly':True}),

     
        }

class RecibirPagoFormNew1(forms.ModelForm):
    class Meta:
        model = RecibirPago
        fields = ('id_reserva', 'monto', 'observaciones')

        labels = {

            'id_reserva':'Reserva',
            'monto':'Monto',
            'observaciones': 'Observaciones'

            }
        widgets= {
      
            'id_reserva': forms.Select(attrs={'class':'form-control','id':'id_reserva'}),
            'monto': forms.TextInput(attrs={'class':'form-control','id':'monto'}),
            'observaciones': forms.TextInput(attrs={'class':'form-control','id':'observaciones'}),

     
        }

class DetalleServicioFormEdit(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ('conductor', 'ubicacion','vehiculo', 'valor', 'fecha_dia',  'fecha_hora','estado_servicio')

        labels = {
            'conductor':'Conductor',
            'ubicacion':'Ubicación',
            'vehiculo':'Vehículo',
            'valor':'Valor',
            'fecha_dia':'Fecha',
            'fecha_hora':'Fecha',
            'estado_servicio':'Estado de Servicio',
            }
        widgets= {
            'conductor': forms.TextInput(attrs={'class':'form-control','id':'conductor'}),
            'ubicacion': forms.TextInput(attrs={'class':'form-control','id':'ubicacion'}),
            'vehiculo': forms.TextInput(attrs={'class':'form-control','id':'vehiculo'}),
            'valor': forms.TextInput(attrs={'class':'form-control','id':'valor'}),
            'fecha_dia': forms.DateInput(format='%Y-%m-%d',attrs={'class':'form-control','id':'fecha_dia','type': 'date'}),
            'fecha_hora': forms.TimeInput(format='%H:%M',attrs={'class':'form-control','id':'fecha_hora','type': 'time'}),
            'estado_servicio': forms.Select(attrs={'class':'form-control','id':'estado_servicio'}),
        }

class ReservaFormNew(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('id_usuario','n_personas', 'n_dias', 'visitantes', 'pago_anticipo', 'pago_faltante', 'pago_multa', 
                   'pago_servicioextra', 'pago_total', 'monto_estadia', 'monto_pordia', 'monto_servicioextra', 
                   'monto_multa', 'monto_total', 'fecha_inicio', 'fecha_termino')

        labels = {
            'id_usuario':'Usuario',
            'n_personas':'Numero de personas',
            'n_dias':'Numero de días',
            'visitantes': 'Visitantes',
            'pago_anticipo': 'Pago Anticipado',
            'pago_faltante': 'Pago Faltante',
            'pago_multa': 'Pago Multa',

            'pago_servicioextra':'Pago Servicio Extra',
            'pago_total':'Pago Total',
            'monto_estadia': 'Monto Estadía',
            'monto_pordia': 'Monto por día',
            'monto_servicioextra': 'Monto Servicio Extra',
            'monto_multa': 'Monto Multa',
            'monto_total': 'Monto Total',
            'fecha_inicio': 'Fecha Inicio',
            'fecha_termino': 'Fecha Término'
            }
        widgets= {
             'id_usuario': forms.Select(attrs={'class':'form-control','id':'id_usuario'}),        
            'n_personas': forms.TextInput(attrs={'class':'form-control','id':'n_personas'}),        
            'n_dias': forms.TextInput(attrs={'class':'form-control','id':'n_dias'}),
            'visitantes': forms.TextInput(attrs={'class':'form-control','id':'visitantes'}),
            'pago_anticipo': forms.TextInput(attrs={'class':'form-control','id':'pago_anticipo'}),
            'pago_faltante': forms.TextInput(attrs={'class':'form-control','id':'pago_faltante'}),
            'pago_multa': forms.TextInput(attrs={'class':'form-control','id':'pago_multa'}),

            'pago_servicioextra': forms.TextInput(attrs={'class':'form-control','id':'pago_servicioextra'}),        
            'pago_total': forms.TextInput(attrs={'class':'form-control','id':'pago_total'}),
            'monto_estadia': forms.TextInput(attrs={'class':'form-control','id':'monto_estadia'}),
            'monto_pordia': forms.TextInput(attrs={'class':'form-control','id':'monto_pordia'}),
            'monto_servicioextra': forms.TextInput(attrs={'class':'form-control','id':'monto_servicioextra'}),
            'monto_multa': forms.TextInput(attrs={'class':'form-control','id':'monto_multa'}),
            'monto_total': forms.TextInput(attrs={'class':'form-control','id':'monto_total'}),

            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
        }

class ReservaInicialPaso2(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('visitantes', 'n_personas')

        labels = {
            'visitantes':'Visitantes',
            'n_personas': 'n_personas'

            }
        widgets= {      
            'visitantes': forms.TextInput(attrs={'class':'form-control','id':'visitantes'}),   
            'n_personas': forms.TextInput(attrs={'class':'form-control','id':'n_personas'}) 
        }            

