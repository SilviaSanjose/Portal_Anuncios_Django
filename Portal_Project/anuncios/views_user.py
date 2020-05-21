''' Vistas Zona de usuario '''
from django.shortcuts import render
from . import models, views, utilidades
import logging 
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from os import remove
from django.utils import timezone

def registrar_anuncio(request):
    res = models.Categoria.objects.order_by("id")
    context = { "categorias": res }
    return render(request, "usuarios/formulario_registro_anuncio.html", context)

def guardar_anuncio(request):
    titulo = request.POST["title"]
    precio = request.POST["price"].replace(",", ".")
    id_categoria = request.POST["category"]
    descripcion = request.POST["message"]
    on_line = request.POST["on_line"]
    new_price = request.POST.get("new_price", False)
    
    usuario = models.Usuario.objects.get(pk = request.session["id_usuario"])    #recojo objeto con el id del usuario en sesion
    anuncio = models.Anuncio(titulo= titulo, precio = precio,  categoria_id = id_categoria, \
                        descripcion =descripcion, on_line = on_line, usuario = usuario, negociable = new_price)
        #categoria_id corresponde al campo del artibuto categoria en tabla de anuncios
        
    anuncio.fecha_modificacion = timezone.now()    #Guardo la fecha de modificación
    anuncio.ip = utilidades.obtener_ip(request)   #guardo la dirección ip
    #guardamos la foto del anuncio
    if "photo" in request.FILES:
        anuncio.foto = True
        anuncio.save()
        id_anuncio = anuncio.id
        ruta = "anuncios/static/images/" + str(id_anuncio) + ".jpg"
        f = request.FILES["photo"]
        default_storage.save(ruta, ContentFile(f.read()))
        
    else:
        anuncio.save()
        
    return render(request, "usuarios/registro_ok.html")

def mis_anuncios(request):
    l = logging.getLogger('django.db.backends')   #mostrar SQL
    l.setLevel(logging.DEBUG)                      
    l.addHandler(logging.StreamHandler()) 

    usuario_logueado = models.Usuario.objects.get(pk = request.session["id_usuario"])
    res = models.Anuncio.objects.filter(usuario = usuario_logueado).prefetch_related('categoria', 'usuario')
    context = {"anuncios" : res }
    return render(request, "usuarios/mis_anuncios.html", context)

def editar_anuncio(request):

    id_editar = request.GET["id_editar"]
    anuncio_editar = models.Anuncio.objects.get(pk = id_editar)
    categoria = models.Categoria.objects.order_by("id")
    context= {"anuncio": anuncio_editar, "categorias": categoria}
    return render(request,"usuarios/edicion_anuncio.html", context)

def guardar_anuncio_editado(request):
    anuncio = models.Anuncio.objects.get(pk = request.POST["id_anuncio"])  #obtengo el objeto/anuncio con id del indicado a editar
    anuncio.titulo = request.POST["title"]                                  #doy los valores del formulario a cada atributo
    anuncio.precio = request.POST["price"].replace(",", ".")
    anuncio.negociable = request.POST.get("new_price", False) 
    anuncio.descripcion = request.POST["message"]
    anuncio.on_line = request.POST["on_line"]
    
    categoria = models.Categoria.objects.get(pk = request.POST["category"])   #recojo la categoria que sea igual al Post del fornulario
    anuncio.categoria = categoria
    anuncio.fecha_modificacion = timezone.now()                 #datetime.now()
    
    #guardamos la foto del anuncio
    if "photo" in request.FILES:
        anuncio.foto = True
        anuncio.save()
        id_anuncio = anuncio.id
        ruta = "anuncios/static/images/" + str(id_anuncio) + ".jpg"
        try: 
            default_storage.delete(ruta)
        except:
            pass
        f = request.FILES["photo"]
        default_storage.save(ruta, ContentFile(f.read()))
    else:
        anuncio.save()
    
    #return redirect("/anuncios/mis-anuncios")
    return mis_anuncios(request)
   
def borrar_anuncio(request):
    id_borrar = request.GET["id_borrar"]
    models.Anuncio.objects.get(pk = id_borrar).delete()
    ruta = "anuncios/static/images/" + str(id_borrar) + ".jpg"
    default_storage.delete(ruta)
    return mis_anuncios(request)
    
def cerrar_sesion(request):
    request.session.clear()
    return views.inicio(request)
