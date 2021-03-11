from django.contrib import admin
from django.urls import path
from .views import *
from .reportes import *



admin.site.site_header = "Administración Turismo Real"
admin.site.site_title = "RentOur"
admin.site.index_title = "Bienvenidos al Panel"


urlpatterns = [

    path('tipo_servicio_lista', ListarTipoServicioExtra.as_view(), name='tipo_servicio_lista'),
    path('crear_detalle_servicio', CrearDetalleServicioExtra.as_view(), name='crear_detalle_servicio'),
    path('reserva_lista', ListarReserva.as_view(), name='reserva_lista'),
    path('crear_checkin/<int:pk>', CrearCheckIn.as_view(), name='crear_checkin'),
    path('ver_checkin/<int:pk>', VerCheckIn.as_view(), name='ver_checkin'),
    path('crear_checkout/<int:pk>', CrearCheckOut.as_view(), name='crear_checkout'),
    path('ver_checkout/<int:pk>', VerCheckOut.as_view(), name='ver_checkout'),
    path('eliminar_tipoServicio/<int:pk>', EliminarTipoServicioExtra.as_view(), name='eliminar_tipoServicio'),
    path('editar_tipoServicio/<str:pk>', ActualizarTipoServicioExtra.as_view(), name='editar_tipoServicio'),
    path('depto_lista_user', depto_Usuario.as_view(), name='depto_lista_user'),
    path('ver_depto/<int:pk>', VerDepto.as_view(), name='ver_depto'),
    path('crear_servicio/<int:pk>', CrearServicioExtra.as_view(), name='crear_servicio'),
    path('cancelar_reserva/<int:pk>', CancelarReserva.as_view(), name='cancelar_reserva'),
    path('reservas_canceladas', ReservasCanceladas.as_view(), name='reservas_canceladas'),
    path('agenda', Ver_Agenda.as_view(), name='agenda'),
    path('lista_pago', ListarPago.as_view(), name='lista_pago'),
    path('reembolso/<int:pk>', Reembolso.as_view(), name='reembolso'),
    path('reservas_reembolso', ReservasReembolso.as_view(), name='reservas_reembolso'),
    path('ver_reserva/<int:pk>', VerReserva.as_view(), name='ver_reserva'),
    path('crear_tipo_servicio', CrearTipoServicioExtra.as_view(), name='crear_tipo_servicio'),

    #RESERVA WEB
    path('lista', Ver_Lista.as_view(), name='lista'),

    #ELEMENTO
    path('elemento_lista', ListarElemento.as_view(), name='elemento_lista'),
    path('elemento_agregar', CrearElemento.as_view(), name='elemento_agregar'),
    path('elemento_eliminar/<int:pk>', EliminarElemento.as_view(), name='elemento_eliminar'),
    path('elemento_editar/<str:pk>', ActualizarElemento.as_view(), name='elemento_editar'),

    #INVENTARIO
    path('inventario_depto', inventario_ver.as_view(), name='inventario_depto'),
    path('crear_inventario/<int:pk>', CrearInventario.as_view(), name='crear_inventario'),
    path('ver_inventario/<int:pk>', VerInventario.as_view(), name='ver_inventario'),
    path('editar_inventario/<str:pk>', ActualizarInventario.as_view(), name='editar_inventario'),
    path('eliminar_inventario/<int:pk>', EliminarInventario.as_view(), name='eliminar_inventario'),

    #DEPARTAMENTO ADMIN
    path('depto_lista', depto_ver.as_view(), name='depto_lista'),
    path('crear_depto', CrearDepto.as_view(), name='crear_depto'),
    path('editar_depto/<int:pk>', ActualizarDepto.as_view(), name='editar_depto'),
    path('eliminar_depto/<int:pk>', EliminarDepto.as_view(), name='eliminar_depto'),
    path('depto_disponibilidad_lista', depto_disponibilidad.as_view(), name='depto_disponibilidad_lista'),
    path('editar_disponibilidad_depto/<str:pk>', ActualizarDisponibilidadDepto.as_view(), name='editar_disponibilidad_depto'),
    
    #TIPO MANTENCION
    path('tm_agregar', CrearTipoMantencion.as_view(), name='tm_agregar'),
    path('tm_lista', tipo_mantencion_lista.as_view(), name='tm_lista'),
    path('tm_eliminar/<int:pk>', EliminarTipoMantencion.as_view(), name='tm_eliminar'),
    path('tm_editar/<str:pk>', ActualizarTipoMantencion.as_view(), name='tm_editar'),
        
    #MANTENCION ADMIN DEPTO
    path('mantencion_eliminar/<int:pk>', EliminarMantencion.as_view(), name='mantencion_eliminar'),

    path('mantencion_actualizar/<str:pk>', ActualizarMantencion.as_view(), name='mantencion_actualizar'),

    path('crear_mantencion/<int:pk>', CrearMantencion.as_view(), name='crear_mantencion'),
    path('ver_mantencion_depto/<int:pk>', VerMantencionDepto.as_view(), name='ver_mantencion_depto'),
    #path('mantencion_lista', depto_Mantencion.as_view(), name='mantencion_lista'),    
    path('mantencion_depto', depto_mantencion_ver.as_view(), name='mantencion_depto'),
    
    #SERVICIO EXTRA RESERVA
    path('detalle_servicio_lista', ListarDetalleServicioExtra.as_view(), name='detalle_servicio_lista'),
    path('editar_detalleServicio/<str:pk>', ActualizarDetalleServicioExtra.as_view(), name='editar_detalleServicio'),
 
    # MANEJO DE RESERVA
    path('crear_reserva/<int:pk>', CrearReserva.as_view(), name='crear_reserva'),
    path('crear_reservaInicial/<int:pk>', CrearReservaInicial.as_view(), name='crear_reservaInicial'),
    path('crear_reserva2/<int:pk>', ActualizarReservaPaso2.as_view(), name='crear_reserva2'),
    path('crear_reserva4/<int:pk>', ActualizarReservaPaso4.as_view(), name='crear_reserva4'),
    path('crear_reserva6/<int:pk>', ActualizarReservaPaso6.as_view(), name='crear_reserva6'),

    # MANEJO DE PAGOS
    path('crear_pago/<int:pk>', CrearPago.as_view(), name='crear_pago'),
    path('crear_pago2/<int:pk>', CrearPago2.as_view(), name='crear_pago2'),
    path('crear_pago3/<int:pk>', CrearPago3.as_view(), name='crear_pago3'),

    # SERVICIOS EXTRAS
    path('eliminar_servicio/<int:pk>', EliminarServicio.as_view(), name='eliminar_servicio'),
    path('servicio_pago/<int:pk>', ServicioPago.as_view(), name='servicio_pago'),
    path('crear_pago_servicio/<int:pk>', CrearPagoServicio.as_view(), name='crear_pago_servicio'),  


    # FUNCIONARIO
    path('entrega',EntregaReserva.as_view(), name='entrega'),
    path('recepcion',RecepcionReserva.as_view(), name='recepcion'),
    path('finalizada',FinalizadaReserva.as_view(), name='finalizada'),

    # CHECK LIST
    path('crear_checklist/<int:pk>', CrearCheckList.as_view(), name='crear_checklist'),
    path('ver_checklist/<int:pk>', VerCheckList.as_view(), name='ver_checklist'),
    path('editar_checklist/<int:pk>', EditarCheckList.as_view(), name='editar_checklist'),

    # PARA DESCARGAR REPORTE
    path('descarga_inventario_reserva/<int:pk>', DescargaInventarioReserva.as_view(), name='descarga_inventario_reserva'),
    path('descarga_reserva/<int:pk>', DescargaReserva.as_view(), name='descarga_reserva'),
    path('descarga_servicio/<int:pk>', DescargaServicio.as_view(), name='descarga_servicio'),
    path('descarga_servicios/<int:pk>', DescargaServicios.as_view(), name='descarga_servicios'),
    path('descarga_inventario/<int:pk>', DescargaInventario.as_view(), name='descarga_inventario'),

    # PARA VER EL REPORTE    
    path('reporte_inventario_reserva/<int:pk>', ReporteInventarioReserva.as_view(), name='reporte_inventario_reserva'),
    path('reporte_reserva/<int:pk>', ReporteReserva.as_view(), name='reporte_reserva'),
    path('reporte_servicio/<int:pk>', ReporteServicio.as_view() ,name="reporte_servicio"),
    path('reporte_servicios/<int:pk>', ReporteServicios.as_view() ,name="reporte_servicios"),
    path('reporte_inventario/<int:pk>', ReporteInventario.as_view(), name='reporte_inventario'),
    
]
