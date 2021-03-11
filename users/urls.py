from django.contrib import admin
from django.urls import path
from .views import *



admin.site.site_header = "Administración Turismo Real"
admin.site.site_title = "RentOur"
admin.site.index_title = "Bienvenidos al Panel"


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('nosotros/', nosotros.as_view(), name='nosotros'),
    path('logout/', logout, name='logout'),
    path('user_lista/', user_ver.as_view(), name='user_lista'),
    path('eliminar_users/<str:pk>', EliminarUsers.as_view(), name='eliminar_users'),
    path('editar_users/<str:pk>', ActualizarUsuario.as_view(), name='editar_users'),


 ]
