from django.urls import path
from . import views, views_user



urlpatterns = [
    path("", views.inicio, name="index"),
    path("registrarse", views.registrarse),
    path("registrar-usuario", views.registrar_usuario),
    path("validar-email", views.validar_email),   
    path("login", views.login),
    path("acceso-usuario", views.acceso_usuario),
    path("buscar-anuncio", views.buscar_anuncio),
    path("contacto-anuncios", views.contacto_anuncios),   
    path("enviar-mensaje", views.enviar_mensaje),  
    #area usuarios
    path("registar-anuncio", views_user.registrar_anuncio),
    path("guardar-anuncio", views_user.guardar_anuncio),
    path("mis-anuncios", views_user.mis_anuncios),
    path("editar-anuncio", views_user.editar_anuncio),
    path("guardar-anuncio-editado", views_user.guardar_anuncio_editado),
    path("borrar-anuncio", views_user.borrar_anuncio),
    path("cerrar-sesion", views_user.cerrar_sesion)
    ]