from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, CreateView,  UpdateView, FormView, ListView, RedirectView
from django.template import RequestContext
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponse

# Create your views here.

class Ver_Lista(LoginRequiredMixin, ListView):
    model = Reserva
    paginate_by = 8
    template_name = 'reserva/mis_reservas.html'
    context_object_name = 'items'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Reserva.objects.all()
        else:
            return Reserva.objects.filter(id_usuario=self.request.user.email, estado_reserva='Nueva')



class Ver_Agenda(LoginRequiredMixin, ListView): 
    model = Reserva
    template_name = 'depto/agenda.html'
    context_object_name = 'items'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Reserva.objects.all()
        else:
            return Reserva.objects.filter(id_usuario=self.request.user.email, estado_reserva='Nueva')




class VerReserva(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        reserva = Reserva.objects.get(id=self.kwargs['pk'])
        #checkin = CheckIn.objects.get(id_reserva=self.kwargs['pk'])
        #checkout = CheckOut.objects.get(id_reserva=self.kwargs['pk'])
        pagos = RecibirPago.objects.filter(id_reserva=self.kwargs['pk'])
        servicios = DetalleServicio.objects.filter(id_reserva=self.kwargs['pk'])
        
        context = {'reserva': reserva, 'pagos': pagos , 'servicios':servicios }
        return render(request, 'reserva/ver_reserva.html', context)

class depto_ver(LoginRequiredMixin, ListView): 
    model = Departamento
    paginate_by = 4
    template_name = 'depto/lista_depto.html'
    queryset = Departamento.objects.all()
    context_object_name = 'items'

class inventario_ver(LoginRequiredMixin, ListView): 
    model = Departamento
    paginate_by = 4
    template_name = 'inventario/inventario_depto.html'
    queryset = Departamento.objects.all()
    context_object_name = 'items'

class depto_mantencion_ver(LoginRequiredMixin, ListView): 
    model = Departamento
    paginate_by = 4
    template_name = 'mantencion/depto_mantencion.html'
    queryset = Departamento.objects.all()
    context_object_name = 'items'



class CrearDepto(LoginRequiredMixin, CreateView):
    model = Departamento
    form_class = DepartamentoFormNew
    template_name = 'depto/agregar_depto.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.estado_depto = 'Nuevo'
        self.object.save()
        return super(CrearDepto, self).form_valid(form)


    def get_success_url(self):
        return reverse_lazy('web:ver_depto', kwargs={'pk': self.object.id_depto})

class ActualizarDepto(LoginRequiredMixin, UpdateView):
    model = Departamento
    template_name = 'depto/editar_depto.html'
    form_class = DepartamentoFormEdit

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('web:ver_depto',pk=pk)

class ActualizarMantencion(LoginRequiredMixin, UpdateView):
    model = Mantencion
    template_name = 'mantencion/mantencion_actualizar.html'
    form_class = EditarMantencion

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('web:ver_mantencion_depto',pk=self.object.id_depto.id_depto)

class ActualizarInventario(LoginRequiredMixin, UpdateView):
    model = Inventario
    template_name = 'inventario/editar_inventario.html'
    form_class = InventarioFormNew

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('web:ver_inventario', pk=self.object.id_depto.id_depto)

class EliminarMantencion(LoginRequiredMixin, ListView):
    model = Mantencion
    template_name = 'mantencion/mantencion_eliminar.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'item': Mantencion.objects.get(id=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        object = Mantencion.objects.get(id=pk)
        id=object.id_depto.id_depto
        object.delete()
        return redirect('web:ver_mantencion_depto',pk=id)


class EliminarDepto(LoginRequiredMixin, ListView):
    model = Departamento
    template_name = 'depto/eliminar_depto.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'depto': Departamento.objects.get(id_depto=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        object = Departamento.objects.get(id_depto=pk)
        object.delete()
        return redirect('web:depto_lista')

class depto_disponibilidad(LoginRequiredMixin, ListView): 
    model = Departamento
    paginate_by = 8
    template_name = 'depto/disponibilidad_depto.html'
    queryset = Departamento.objects.all()
    context_object_name = 'items'

class ActualizarDisponibilidadDepto(LoginRequiredMixin, UpdateView):
    model = Departamento
    template_name = 'depto/editar_disponibilidad.html'
    form_class = DepartamentoDisponibilidadFormEdit
    success_url = reverse_lazy('web:depto_disponibilidad_lista')

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('web:depto_disponibilidad_lista')

class CrearTipoMantencion(LoginRequiredMixin, CreateView):
    model = TipoMantencion
    form_class = TipoMantencionFormNew
    success_url = reverse_lazy('web:tm_lista')
    template_name = 'mantencion/tm_agregar.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)        
        #self.object.user_id = User.objects.get(id=self.request.user.id)
        self.object.save()
        return super(CrearTipoMantencion, self).form_valid(form)

class CrearMantencion(LoginRequiredMixin, CreateView):
    model = Mantencion
    form_class = MantencionFormNew
    template_name = 'mantencion/depto_agregar_mantencion.html'
    

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        form = MantencionFormNew(initial={'id_depto':depto})
        context = {'form': form, 'depto':depto}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        self.object = form.save(commit=False)
        self.object.id_depto=depto
        self.object.save()
        return super(CrearMantencion, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('web:ver_mantencion_depto', kwargs={'pk': self.kwargs['pk']})

class VerMantencionDepto(LoginRequiredMixin, ListView): 
    model = Mantencion
    paginate_by = 4
    template_name = 'mantencion/depto_mantencion_ver.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        items2=Mantencion.objects.filter(id_depto=pk,estado_mantencion='Realizado')
        context = super().get_context_data(**kwargs)
        context['items2'] = items2
        context['depto'] = depto
        return context

    def get_queryset(self):
        return Mantencion.objects.filter(id_depto=self.request.resolver_match.kwargs['pk'],estado_mantencion='Nueva')

class depto_Mantencion(LoginRequiredMixin, ListView): 
    model = Departamento
    paginate_by = 8
    template_name = 'mantencion/depto_lista_mantencion.html'
    queryset = Departamento.objects.filter(estado_depto="Mantencion")
    context_object_name = 'items'

class tipo_mantencion_lista(LoginRequiredMixin, ListView): 
    model = TipoMantencion
    paginate_by = 8
    template_name = 'mantencion/tm_lista.html'
    queryset = TipoMantencion.objects.all()
    context_object_name = 'items'

class CrearTipoServicioExtra(LoginRequiredMixin, CreateView):
    model = TipoServicioExtra
    form_class = TipoServicioExtraFormNew
    success_url = reverse_lazy('web:tipo_servicio_lista')
    template_name = 'servicio/agregar_tipoServicio.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(CrearTipoServicioExtra, self).form_valid(form)

class ListarTipoServicioExtra(LoginRequiredMixin, ListView): 
    model = TipoServicioExtra
    paginate_by = 4
    template_name = 'servicio/listar_tipoServicio.html'
    queryset = TipoServicioExtra.objects.all()
    context_object_name = 'items'

class CrearDetalleServicioExtra(LoginRequiredMixin, CreateView):
    model = DetalleServicio
    form_class = DetalleServicioFormNew
    success_url = reverse_lazy('web:detalle_servicio_lista')
    template_name = 'servicio/agregar_detalleServicio.html'

    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)

class ListarDetalleServicioExtra(LoginRequiredMixin, ListView): 
    model = DetalleServicio
    template_name = 'servicio/listar_detalleServicio.html'
    queryset = DetalleServicio.objects.all()
    context_object_name = 'items'


class ListarElemento(LoginRequiredMixin, ListView): 
    model = Elemento
    paginate_by = 4
    template_name = 'inventario/elemento_lista.html'
    queryset = Elemento.objects.all()
    context_object_name = 'items'

class CrearElemento(LoginRequiredMixin, CreateView):
    model = Elemento
    form_class = ElementoFormNew
    success_url = reverse_lazy('web:elemento_lista')
    template_name = 'inventario/elemento_agregar.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(CrearElemento, self).form_valid(form)

class CrearInventario(LoginRequiredMixin, CreateView):
    model = Inventario
    form_class = InventarioFormNew
    template_name = 'inventario/agregar_inventario_depto.html'
    

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        form = InventarioFormNew(initial={'id_depto':depto})
        context = {'form': form, 'depto':depto}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        self.object = form.save(commit=False)
        self.object.id_depto=depto
        self.object.save()
        return super(CrearInventario, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('web:ver_inventario', kwargs={'pk': self.kwargs['pk']})

class VerInventario(LoginRequiredMixin, ListView): 
    model = Inventario
    paginate_by = 4
    template_name = 'inventario/ver_inventario.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        context = super().get_context_data(**kwargs)
        context['depto'] = depto
        return context

    def get_queryset(self):
        return Inventario.objects.filter(id_depto=self.request.resolver_match.kwargs['pk'])


class ListarReserva(LoginRequiredMixin, ListView): 
    model = Reserva
    paginate_by = 4
    template_name = 'reserva/lista_reservas.html'
    queryset = Reserva.objects.all()
    context_object_name = 'items'

class EntregaReserva(LoginRequiredMixin, ListView): 
    model = Reserva
    paginate_by = 4
    template_name = 'funcionario/entrega.html'
    queryset = Reserva.objects.filter(estado_reserva='Nueva')
    context_object_name = 'items'

class RecepcionReserva(LoginRequiredMixin, ListView): 
    model = Reserva
    paginate_by = 4
    template_name = 'funcionario/recepcion.html'
    queryset = Reserva.objects.filter(estado_reserva='En uso')
    context_object_name = 'items'

class FinalizadaReserva(LoginRequiredMixin, ListView): 
    model = Reserva
    paginate_by = 4
    template_name = 'funcionario/finalizada.html'
    queryset = Reserva.objects.filter(estado_reserva='Finalizada')
    context_object_name = 'items'

class CrearCheckIn(LoginRequiredMixin, CreateView):
    model = CheckIn
    form_class = CheckInFormNew
    template_name = 'funcionario/crear_checkin.html'
    

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        form = CheckInFormNew(initial={'id':reserva})
        context = {'form': form, 'reserva':reserva}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        self.object = form.save(commit=False)
        self.object.id_reserva=reserva
        self.object.save()
        return super(CrearCheckIn, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('web:ver_checkin', kwargs={'pk': self.kwargs['pk']})

class VerCheckIn(LoginRequiredMixin, UpdateView): 
    model = CheckIn
    template_name = 'funcionario/ver_checkin.html'
    form_class = CheckInFormNew
    success_url = reverse_lazy('web:entrega')

   
    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        comprobar_uso(self.object)

        return redirect('web:entrega')
        

class EditarCheckList(LoginRequiredMixin, UpdateView): 
    model = CheckList
    template_name = 'funcionario/editar_checklist.html'
    form_class = CheckListFormEdit

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        detalle = CheckList.objects.get(id=pk)
        kwargs['detalle'] = detalle

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.check = True

        multa = 0
        multa_actual = self.object.monto_multa
        multa_unidad = self.object.id_inventario.id_elemento.valor

        diferencia = self.object.id_inventario.cantidad - self.object.cantidad_real
        if diferencia > 0:
            multa = multa_unidad * diferencia 

        diferencia_multa = multa - multa_actual
        if diferencia_multa != 0:
            #agregar diferencia de multa a CheckOut
            checkout = CheckOut.objects.get(id_reserva=self.object.id_reserva)
            checkout.total_multa = checkout.total_multa + diferencia_multa
            checkout.save()

            reserva = checkout.id_reserva
            reserva.monto_multa = checkout.total_multa
            reserva.monto_total = reserva.monto_estadia + reserva.monto_servicioextra + reserva.monto_multa
            reserva.save()

            print(diferencia_multa)

        self.object.monto_multa = multa
        self.object.save()
        return redirect('web:ver_checklist',pk=self.object.id_reserva.id)
    

class CrearCheckList(LoginRequiredMixin, CreateView):
    model = CheckList
    form_class = CheckListFormNew
    template_name = 'funcionario/crear_checklist.html'
    

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        form = CheckListFormNew(initial={'id':reserva})
        context = {'form': form, 'reserva':reserva}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        self.object = form.save(commit=False)
        self.object.id_reserva=reserva
        self.object.save()
        return super(CrearCheckList, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('web:ver_checklist', kwargs={'pk': self.kwargs['pk']})

class VerCheckList(LoginRequiredMixin, View): 
    template_name = 'funcionario/ver_checklist.html'

    def get(self, request, *args, **kwargs):        
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        items = CheckList.objects.filter(id_reserva=reserva.id)
        context = {'reserva' : reserva, 'items': items}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        pk = self.kwargs['pk']        
        print('pk'+str(pk))

        return redirect('web:ver_checklist', pk=pk)

class CrearCheckOut(LoginRequiredMixin, CreateView):
    model = CheckOut
    form_class = CheckOutFormNew
    template_name = 'funcionario/crear_checkout.html'
    

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        form = CheckOutFormNew(initial={'id':reserva})
        context = {'form': form, 'reserva':reserva}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        self.object = form.save(commit=False)
        self.object.id_reserva=reserva
        self.object.save()
        return super(CrearCheckOut, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('web:ver_checkout', kwargs={'pk': self.kwargs['pk']})

class VerCheckOut(LoginRequiredMixin, UpdateView): 
    model = CheckOut
    template_name = 'funcionario/ver_checkout.html'
    form_class = CheckOutFormNew
    success_url = reverse_lazy('web:recepcion')

   
    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        comprobar_cierre(self.object)
        return redirect('web:recepcion')

class EliminarTipoMantencion(LoginRequiredMixin, ListView):
    model = TipoMantencion
    template_name = 'mantencion/tm_eliminar.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'tipoM': TipoMantencion.objects.get(id=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        object = TipoMantencion.objects.get(id=pk)
        object.delete()
        return redirect('web:tm_lista')

class ActualizarTipoMantencion(LoginRequiredMixin, UpdateView):
    model = TipoMantencion
    template_name = 'mantencion/tm_agregar.html'
    form_class = TipoMantencionFormNew
    success_url = reverse_lazy('web:tm_lista')

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('web:tm_lista')

class EliminarElemento(LoginRequiredMixin, ListView):
    model = Elemento
    template_name = 'inventario/elemento_eliminar.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'elemento': Elemento.objects.get(id=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        object = Elemento.objects.get(id=pk)
        object.delete()
        return redirect('web:elemento_lista')

class ActualizarElemento(LoginRequiredMixin, UpdateView):
    model = Elemento
    template_name = 'inventario/elemento_agregar.html'
    form_class = ElementoFormNew
    success_url = reverse_lazy('web:elemento_lista')

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('web:elemento_lista')

class EliminarInventario(LoginRequiredMixin, ListView):
    model = Inventario
    template_name = 'inventario/eliminar_inventario.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'inventario': Inventario.objects.get(id=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        object = Inventario.objects.get(id=pk)
        id = object.id_depto.id_depto
        object.delete()
        return redirect('web:ver_inventario', pk=id)


class EliminarTipoServicioExtra(LoginRequiredMixin, ListView):
    model = TipoServicioExtra
    template_name = 'servicio/eliminar_tipoServicio.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'tipo_servicio': TipoServicioExtra.objects.get(id=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        object = TipoServicioExtra.objects.get(id=pk)
        object.delete()
        return redirect('web:tipo_servicio_lista')

class ActualizarTipoServicioExtra(LoginRequiredMixin, UpdateView):
    model = TipoServicioExtra
    template_name = 'servicio/agregar_tipoServicio.html'
    form_class = TipoServicioExtraFormNew
    success_url = reverse_lazy('web:tipo_servicio_lista')

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('web:tipo_servicio_lista')

class ActualizarDetalleServicioExtra(LoginRequiredMixin, UpdateView):
    model = DetalleServicio
    template_name = 'servicio/editar_detalleServicio.html'
    form_class = DetalleServicioFormEdit
    success_url = reverse_lazy('web:detalle_servicio_lista')

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        detalle = DetalleServicio.objects.get(id=pk)
        kwargs['detalle'] = detalle

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('web:detalle_servicio_lista')


class depto_Usuario(LoginRequiredMixin, ListView): 
    model = Departamento
    paginate_by = 4
    template_name = 'reserva/lista_deptos.html'
    queryset = Departamento.objects.all()
    context_object_name = 'items'

class CrearReserva(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaFormNew
    template_name = 'reserva/crear_reserva.html'
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        form = ReservaFormNew(initial={'id_depto':depto})
        context = {'form': form, 'depto':depto}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        self.object = form.save(commit=False)
        self.object.id_depto=depto
        self.object.save()
        return super(CrearReserva, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('web:reserva_lista')

class CrearReservaInicial(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaInicialPaso1
    template_name = 'reserva/crear_reserva.html'
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        form = ReservaInicialPaso1(initial={'id_depto':depto})
        context = {'form': form, 'depto':depto}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        
        self.object = form.save(commit=False)
        self.object.id_depto=depto
        self.object.monto_pordia  = depto.valor_arriendo
        self.object.estado_reserva='Solicitud'
        self.object.id_usuario = self.request.user
        self.object.save()
       
        return super().form_valid(form)
        # return reverse_lazy('web:crear_reserva2', kwargs={'solicitud': self.object})

    def get_success_url(self):
        return reverse_lazy('web:crear_reserva2', kwargs={'pk': self.object.id})


class ActualizarReservaPaso2(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        objeto = Reserva.objects.get(id=self.kwargs['pk'])
        objeto.monto_estadia = objeto.n_dias*objeto.monto_pordia
        objeto.monto_total = objeto.monto_estadia + objeto.monto_servicioextra + objeto.monto_multa
        monto = objeto.id_depto.pct_anticipo*objeto.monto_estadia/100
        objeto.fecha_termino = objeto.fecha_inicio + datetime.timedelta(days=objeto.n_dias)
        objeto.save()
        context = {'reserva': objeto, 'monto': monto}
        return render(request, 'reserva/crear_reserva2.html', context)


class ActualizarReservaPaso4(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        objeto = Reserva.objects.get(id=self.kwargs['pk'])
        monto = objeto.monto_estadia - objeto.pago_anticipo
        context = {'reserva': objeto, 'monto': monto}
        return render(request, 'reserva/crear_reserva4.html', context)



class ActualizarReservaPaso6(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        objeto = Reserva.objects.get(id=self.kwargs['pk'])
        monto = objeto.monto_multa
        context = {'reserva': objeto, 'monto': monto}
        return render(request, 'reserva/crear_reserva6.html', context)


class VerDepto(LoginRequiredMixin, ListView): 
    model = Departamento
    paginate_by = 4
    template_name = 'reserva/vista_reserva.html'
    context_object_name = 'items'
 
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        depto = Departamento.objects.get(id_depto=pk)
        context = super().get_context_data(**kwargs)
        context['depto'] = depto
        return context
 
    def get_queryset(self):
        return Departamento.objects.filter(id_depto=self.request.resolver_match.kwargs['pk'])


class CrearServicioExtra(LoginRequiredMixin, CreateView):
    model = DetalleServicio
    form_class = DetalleServicioFormNew
    template_name = 'reserva/crear_Servicioextra.html'
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        depto = reserva.id_depto
        form = DetalleServicioFormNew(initial={'id_reserva':reserva, 'id_depto':depto})
        context = {'form': form, 'reserva':reserva}
        return render(request, self.template_name, context)
    

    def form_valid(self, form):
        pk = self.kwargs['pk']
        reserva = Reserva.objects.get(id=pk)
        self.object = form.save(commit=False)
        self.object.id_reserva=reserva        
        self.object.estado_servicio = 'Solicitud'
        self.object.save()
        return super(CrearServicioExtra, self).form_valid(form)

    def get_success_url(self):        
        return reverse_lazy('web:ver_reserva', kwargs={'pk': self.object.id_reserva.id})

 
class EliminarServicio(LoginRequiredMixin, ListView):
    model = DetalleServicio
    template_name = 'servicio/eliminar_detalleServicio.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'detalle': DetalleServicio.objects.get(id=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        temp = DetalleServicio.objects.get(id=pk)
        reserva = temp.id_reserva
        temp.delete()
        return redirect('web:ver_reserva', pk=reserva.id)


class  EliminarServicio2(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        try:
            temp = DetalleServicio.objects.get(id=pk)
            reserva = temp.id_reserva
            temp.delete()
        except DetalleServicio.DoesNotExist:
            print("Hola")
        #checkin = CheckIn.objects.get(id_reserva=self.kwargs['pk'])
        #checkout = CheckOut.objects.get(id_reserva=self.kwargs['pk'])
        pagos = RecibirPago.objects.filter(id_reserva=reserva.id)
        servicios = DetalleServicio.objects.filter(id_reserva=reserva.id)
        
        context = {'reserva': reserva, 'pagos': pagos , 'servicios':servicios }
        return render(request, 'reserva/ver_reserva.html', context)


class CancelarReserva(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reserva/cancelar_reserva.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'reserva': Reserva.objects.get(id=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        objeto = Reserva.objects.get(id=self.kwargs['pk'])
        objeto.estado_reserva = 'Anulada'
        objeto.save()
        return redirect('web:lista')

class ReservasCanceladas(LoginRequiredMixin, ListView): 
    model = Reserva
    paginate_by = 4
    template_name = 'reserva/reserva_cancelada.html'
    queryset = Reserva.objects.filter(estado_reserva='Anulada')
    context_object_name = 'items'

class ReservasReembolso(LoginRequiredMixin, ListView): 
    model = Reserva
    paginate_by = 4
    template_name = 'reserva/reserva_reembolso.html'
    queryset = Reserva.objects.filter(estado_reserva='Reembolsado')
    context_object_name = 'items'

class Reembolso(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reserva/reembolso.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'reserva': Reserva.objects.get(id=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        objeto = Reserva.objects.get(id=self.kwargs['pk'])
        objeto.estado_reserva = 'Reembolsado'
        objeto.save()
        reembolso(objeto)
        return redirect('web:reservas_reembolso')

class ServicioPago(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        print("estoy get")
        pk = self.kwargs['pk']
        servicio = DetalleServicio.objects.get(id=pk)        
        context = {'servicio':servicio}
        return render(request,  'servicio/servicio_pago1.html',  context)

class CrearPagoServicio(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        print("estoy get")
        pk = self.kwargs['pk']
        servicio = DetalleServicio.objects.get(id=pk)
        servicio.estado_servicio = 'Pagado'
        servicio.check_pago = True        
        servicio.save()
        recibir = pago_servicio(servicio)
        context = {'servicio':servicio,'recibir':recibir}
        return render(request,  'servicio/crear_pago_servicio.html',  context)



class CrearPago(LoginRequiredMixin, View):
    template_name = 'reserva/crear_reserva3.html'
    

    def get(self, request, *args, **kwargs):
        print("estoy get")
        pk = self.kwargs['pk']


        reserva = Reserva.objects.get(id=pk)
        reserva.estado_reserva = 'Nueva'        
        monto_anticipo = reserva.id_depto.pct_anticipo*reserva.monto_estadia/100
        reserva.pago_anticipo = monto_anticipo
        reserva.save()

        recibir = pago_anticipo(reserva)
        crear_checklist(reserva)
        crear_checkin(reserva)
        crear_checkout(reserva)
        
        context = {'reserva':reserva,'recibir':recibir}
        return render(request, self.template_name, context)



class CrearPago2(LoginRequiredMixin, View):
    template_name = 'reserva/crear_reserva5.html'
    

    def get(self, request, *args, **kwargs):
        print("estoy get")
        pk = self.kwargs['pk']


        reserva = Reserva.objects.get(id=pk)  
        monto = reserva.monto_estadia - reserva.pago_anticipo
        reserva.pago_faltante = monto
        reserva.save()

        recibir = pago_faltante(reserva)
        check_estadia(reserva)
        
        context = {'reserva':reserva,'recibir':recibir}
        return render(request, self.template_name, context)



class CrearPago3(LoginRequiredMixin, View):
    template_name = 'reserva/crear_reserva7.html'
    

    def get(self, request, *args, **kwargs):
        print("estoy get")
        pk = self.kwargs['pk']


        reserva = Reserva.objects.get(id=pk)  
        monto = reserva.monto_multa
        reserva.pago_multa = monto
        reserva.save()

        recibir = pago_multa(reserva)
        check_multa(reserva)
        
        context = {'reserva':reserva,'recibir':recibir}
        return render(request, self.template_name, context)



class ListarPago(LoginRequiredMixin, ListView): 
    model = RecibirPago
    paginate_by = 4
    template_name = 'reporte/lista_pago.html'
    context_object_name = 'items'

def check_estadia(reserva):
    objeto=CheckIn.objects.get(id_reserva=reserva)
    objeto.check_pago = True
    objeto.save()

def check_multa(reserva):
    objeto=CheckOut.objects.get(id_reserva=reserva)
    objeto.check_multa = True
    objeto.check_lista = True
    objeto.detalle_multa = "Pago de Multas - OK"
    objeto.save()

def crear_checklist(reserva):
    
    lista=Inventario.objects.filter(id_depto=reserva.id_depto)
    for item in lista:
        print(item)
        temp=CheckList()
        temp.id_reserva = reserva
    
        temp.id_inventario = item
        try:
            objeto=CheckList.objects.get(id_reserva=reserva,id_inventario=item)
        except CheckList.DoesNotExist:
            temp.save()

def crear_checkin(reserva):
  
    temp=CheckIn()
    temp.id_reserva = reserva
    
    try:
        objeto=CheckIn.objects.get(id_reserva=reserva)
    except CheckIn.DoesNotExist:
        temp.save()

def crear_checkout(reserva):
    
    temp=CheckOut()
    temp.id_reserva = reserva
   
    try:
        objeto=CheckOut.objects.get(id_reserva=reserva)
    except CheckOut.DoesNotExist:
        temp.save()


def pago_faltante(reserva):
    recibir = RecibirPago()
    recibir.id_reserva = reserva
    recibir.monto = reserva.pago_faltante
    obs = "Pago Estadía Faltante"
    recibir.observaciones = obs
    try:
        objeto=RecibirPago.objects.get(id_reserva=reserva,observaciones="Pago Estadía Faltante")
    except RecibirPago.DoesNotExist:
        reserva.pago_total = reserva.pago_total + recibir.monto
        reserva.save()
        recibir.save()
    return recibir 

def pago_anticipo(reserva):
    recibir = RecibirPago()
    recibir.id_reserva = reserva
    recibir.monto = reserva.pago_anticipo
    obs = "Pago Anticipo"
    recibir.observaciones = obs
    try:
        objeto=RecibirPago.objects.get(id_reserva=reserva,observaciones="Pago Anticipo")
    except RecibirPago.DoesNotExist:
        reserva.pago_total = reserva.pago_total + recibir.monto
        reserva.save()
        recibir.save()        
    return recibir 

def comprobar_uso(checkin):
    reserva = checkin.id_reserva
    if checkin.check_pago ==True and checkin.check_lista ==True and checkin.check_pdf ==True and checkin.check_servicio ==True and checkin.check_llave ==True:
        reserva.estado_reserva = 'En uso'
    else:
        reserva.estado_reserva = 'Nueva'
    reserva.save()

def comprobar_cierre(checkout):
    reserva = checkout.id_reserva
    if checkout.check_lista==True and checkout.check_multa==True and checkout.check_pdf==True :
        reserva.estado_reserva = 'Finalizada'
    else:
        reserva.estado_reserva = 'En uso'
    reserva.save()

def reembolso(reserva):
    objeto=RecibirPago.objects.filter(id_reserva=reserva).exclude(observaciones='Reembolso')
    temp=0
    for item in objeto:
        temp= temp-item.monto
    reembolso = RecibirPago()
    reembolso.id_reserva = reserva
    reembolso.monto = temp
    obs = "Reembolso"
    reembolso.observaciones = obs
    try:
        objeto=RecibirPago.objects.get(id_reserva=reserva,observaciones="Reembolso")
    except RecibirPago.DoesNotExist:        
        reserva.pago_total = reserva.pago_total + reembolso.monto
        reserva.save()
        reembolso.save() 


def pago_servicio(servicio):
    recibir = RecibirPago()
    recibir.id_reserva = servicio.id_reserva
    recibir.id_detalleservicio = servicio
    recibir.monto = servicio.valor
    obs = "Pago Servicio Extra"
    recibir.observaciones = obs
    try:
        objeto=RecibirPago.objects.get(id_detalleservicio=servicio.id,observaciones="Pago Servicio Extra")
    except RecibirPago.DoesNotExist:
        reserva = servicio.id_reserva

        reserva.monto_servicioextra = reserva.monto_servicioextra + servicio.valor
        reserva.monto_total = reserva.monto_estadia + reserva.monto_servicioextra + reserva.monto_multa

        reserva.pago_servicioextra = reserva.pago_servicioextra + servicio.valor
        reserva.pago_total = reserva.pago_total + recibir.monto

        reserva.save()
        recibir.save()
    return recibir 


def pago_multa(reserva):
    recibir = RecibirPago()
    recibir.id_reserva = reserva
    recibir.monto = reserva.pago_multa
    obs = "Pago Multa"
    recibir.observaciones = obs
    try:
        objeto=RecibirPago.objects.get(id_reserva=reserva,observaciones="Pago Multa")
    except RecibirPago.DoesNotExist:

        reserva.pago_total = reserva.pago_total + recibir.monto
        reserva.monto_total = reserva.monto_estadia + reserva.monto_servicioextra + reserva.monto_multa

        reserva.save()
        recibir.save()        
    return recibir 
