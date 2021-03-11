from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as do_logout
from django.shortcuts import render, redirect
from users.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, CreateView,  UpdateView, FormView, ListView, RedirectView
from .models import *
from django.urls import reverse_lazy
from web.models import *
from datetime import datetime
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.utils.safestring import SafeString



def index(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "users/welcome.html")
    # En otro caso redireccionamos al login

    return render(request, "index.html")

class Inicio(ListView):
    model = Departamento
    paginate_by = 4
    template_name = 'index.html'
    queryset = Departamento.objects.all()
    context_object_name = 'items'
    

class admin_base(LoginRequiredMixin,TemplateView):
    template_name = 'admin_base.html'

    def get_grafico(self):
        data = []
        year = datetime.now().year
        
        for m in range(1, 13):
            total = RecibirPago.objects.filter(fecha__year=year, fecha__month=m).aggregate(r=Coalesce(Sum('monto'), 0)).get('r')
            data.append(float(total))

        return data
    
    def get_grafico_semanal(self):
        data = []
        year = datetime.now().month
        
        for m in range(1, 32):
            total = RecibirPago.objects.filter(fecha__month=year, fecha__day=m).aggregate(r=Coalesce(Sum('monto'), 0)).get('r')
            data.append(float(total))

        return data

    def get_grafico_norte(self):
        data = []
        year = datetime.now().year
        
        for m in range(1, 13):
            total = RecibirPago.objects.filter(fecha__year=year, fecha__month=m, id_reserva__id_depto__zona='Norte').aggregate(r=Coalesce(Sum('monto'), 0)).get('r')
            data.append(float(total))

        return data
    
    def get_grafico_litoral(self):
        data = []
        year = datetime.now().year
        
        for m in range(1, 13):
            total = RecibirPago.objects.filter(fecha__year=year, fecha__month=m, id_reserva__id_depto__zona='Litoral').aggregate(r=Coalesce(Sum('monto'), 0)).get('r')
            data.append(float(total))

        return data
    
    def get_grafico_sur(self):
        data = []
        year = datetime.now().year
        
        for m in range(1, 13):
            total = RecibirPago.objects.filter(fecha__year=year, fecha__month=m, id_reserva__id_depto__zona='Sur').aggregate(r=Coalesce(Sum('monto'), 0)).get('r')
            data.append(float(total))

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grafico'] = self.get_grafico()
        context['grafico_semanal'] = self.get_grafico_semanal()
        context['grafico_norte'] = self.get_grafico_norte()
        context['grafico_litoral'] = self.get_grafico_litoral()
        context['grafico_sur'] = self.get_grafico_sur()

        return context

  

class nosotros(TemplateView):
    template_name = 'nosotros.html'

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "users/welcome.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def register(request):
    # Creamos el formulario de autenticación vacío
    form = UsuarioCreateForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UsuarioCreateForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})


def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html", {'form': form})


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

class user_ver(LoginRequiredMixin, ListView): 
    model = Usuario
    paginate_by = 20
    template_name = 'users/lista_user.html'
    queryset = Usuario.objects.all()
    context_object_name = 'items'

# class CrearFuncionario(LoginRequiredMixin, CreateView):
#     model = Usuario
#     form_class = UsuarioFuncionarioFormNew
#     success_url = reverse_lazy('users:user_lista')
#     template_name = 'users/agregar_funcionario.html'

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.is_staff = True
#         #self.object.user_id = User.objects.get(id=self.request.user.id)
#         self.object.save()
#         return super(CrearFuncionario, self).form_valid(form)

class EliminarUsers(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'users/eliminar_users.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        contexto = {
            'users': Usuario.objects.get(email=pk),
            'pk': pk,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, pk, *args, **kwargs):
        object = Usuario.objects.get(email=pk)
        object.delete()
        return redirect('users:user_lista')

class ActualizarUsuario(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'users/editar_users.html'
    form_class = UsuarioFormEdit
    success_url = reverse_lazy('users:user_lista')

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('users:user_lista')