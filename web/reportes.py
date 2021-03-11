import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, CreateView,  UpdateView, FormView, ListView, RedirectView
from django.template import RequestContext
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.staticfiles import finders

# INVENTARIO DEL DEPARTAMENTO

class DescargaInventario(View):
    template_name = get_template('reporte/reporte_inventario.html')

    def get(self, request, *args, **kwargs):
        context = contextoInventario(self.kwargs['pk'])
        html = self.template_name.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

def contextoInventario(id_depto):
    inventario = Inventario.objects.filter(id_depto=id_depto)
    context = {
        'comp': {'name': 'TURISMO-RENTOUR S.A.', 'ruc': '2017201820192020', 'address': 'PROVIDENCIA #2020, CHILE'},
        'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png'),
        'inventario': inventario}
    return context

class ReporteInventario(LoginRequiredMixin, View):
    template_name = 'reporte/reporte_inventario.html'

    def get(self, request, *args, **kwargs):
        context = contextoInventario(self.kwargs['pk'])
        return render(request, self.template_name, context)

# RESERVA

class DescargaReserva(View):
    template_name = get_template('reporte/reporte_reserva.html')

    def get(self, request, *args, **kwargs):
        context = contextoReserva(self.kwargs['pk']) # OBTENER SERVICIOS
        html = self.template_name.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

class ReporteReserva(LoginRequiredMixin, View):
    template_name = 'reporte/reporte_reserva.html'

    def get(self, request, *args, **kwargs):
        context = contextoReserva(self.kwargs['pk'])
        return render(request, self.template_name, context)


def contextoReserva(id_reserva):
    reserva = Reserva.objects.get(id=id_reserva)

    check =CheckIn.objects.get(id_reserva=reserva.id)
    check.check_pdf = True
    check.save()

    context = {
        'comp': {'name': 'TURISMO-RENTOUR S.A.', 'ruc': '2017201820192020', 'address': 'PROVIDENCIA #2020, CHILE'},
        'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png'),
        'reserva': reserva}
    return context

# DETALLES DE SERVICIOS DE UNA RESERVA

class DescargaServicios(View):
    template_name = get_template('reporte/reporte_servicios.html')

    def get(self, request, *args, **kwargs):
        context = contextoServicios(self.kwargs['pk']) # OBTENER SERVICIOS
        html = self.template_name.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

class ReporteServicios(LoginRequiredMixin, View):
    template_name = 'reporte/reporte_servicios.html'

    def get(self, request, *args, **kwargs):      
        context = contextoServicios( self.kwargs['pk'])
        return render(request, self.template_name, context)

def contextoServicios(id_reserva):
    reserva = Reserva.objects.get(id=id_reserva)    
    servicios = DetalleServicio.objects.filter(id_reserva=reserva.id)
    
    check =CheckIn.objects.get(id_reserva=reserva.id)
    check.check_servicio = True
    check.save()

    context = {
        'comp': {'name': 'TURISMO-RENTOUR S.A.', 'ruc': '2017201820192020', 'address': 'PROVIDENCIA #2020, CHILE'},
        'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png'),
        'servicios': servicios}
    return context

# DETALLE SERVICIO

class DescargaServicio(View):
    template_name = get_template('reporte/reporte_reserva.html')

    def get(self, request, *args, **kwargs):
        context = contextoServicio(self.kwargs['pk']) # OBTENER SERVICIO
        html = self.template_name.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

class ReporteServicio(LoginRequiredMixin, View):
    template_name = 'reporte/reporte_reserva.html'

    def get(self, request, *args, **kwargs):
        context = contextoServicio(self.kwargs['pk'])
        return render(request, self.template_name, context)

def contextoServicio(id_detalleServicio):
    objeto = DetalleServicio.objects.get(id=id_detalleServicio)
    context = {
    'comp': {'name': 'TURISMO-RENTOUR S.A.', 'ruc': '2017201820192020', 'address': 'PROVIDENCIA #2020, CHILE'},
    'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png'),
    'servicio': objeto}
    return context


    
# INVENTARIO DEL DEPARTAMENTO DE LA RESERVA

class DescargaInventarioReserva(View):
    template_name = get_template('reporte/reporte_inventario_reserva.html')

    def get(self, request, *args, **kwargs):
        context = contextoInventarioReserva(self.kwargs['pk'])
        html = self.template_name.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

def contextoInventarioReserva(id_reserva):
    reserva = Reserva.objects.get(id=id_reserva)
    listaCheckList = CheckList.objects.filter(id_reserva=reserva.id)
    
    check =CheckIn.objects.get(id_reserva=reserva.id)
    check.check_lista = True
    check.save()

    context = {
        'comp': {'name': 'TURISMO-RENTOUR S.A.', 'ruc': '2017201820192020', 'address': 'PROVIDENCIA #2020, CHILE'},
        'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png'),
        'lista': listaCheckList,
        'depto': reserva.id_depto}
    return context

class ReporteInventarioReserva(LoginRequiredMixin, View):
    template_name = 'reporte/reporte_inventario_reserva.html'

    def get(self, request, *args, **kwargs):
        context = contextoInventarioReserva(self.kwargs['pk'])
        return render(request, self.template_name, context)
