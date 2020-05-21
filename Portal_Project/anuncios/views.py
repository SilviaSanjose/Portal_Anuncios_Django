from django.shortcuts import render
from . import models
import logging   #mostrar las sql que lanza django
from django.core.mail import send_mail, EmailMultiAlternatives     #envio de emails
from django.conf import settings
import random, string


# Create your views here.

def inicio(request):
    '''
    #prueba para ver la información que puedo sacar el usuario actual:
    texto = "info del usuario: "
    ip = utilidades.obtener_ip(request)
    texto += ip
    return HttpResponse(texto)'''
    
    l = logging.getLogger('django.db.backends')   
    l.setLevel(logging.DEBUG)                     
    l.addHandler(logging.StreamHandler())           #que muestre directamente por consola 
    
    res = models.Anuncio.objects.order_by("-id").prefetch_related('categoria', 'usuario')    
    context = { "anuncios": res}
    return render(request, "index.html", context)

def registrarse(request):
    return render(request, "registrarse.html")

def registrar_usuario(request):
    user = request.POST["user"]
    email = request.POST["email"].lower().strip()
    passwd= request.POST["passwd"]
    
    res = models.Usuario.objects.filter(email = email)    #compruebo si el email que dan ya existe en db.
    if len(res) == 1:    #si es 1 es porque ha devuelto un registro
        context ={ "error_email" : "Ese email ya existe"}
        return render(request, "registrarse.html", context)
    else: 
        codigo = ''.join(random.choices(string.ascii_letters + string.digits, k= 200))     #genero código de verificación
        new_user = models.Usuario(usuario= user, email = email, contraseña = passwd, codigo=codigo)
        if "photo" in request.FILES:
            new_user.imagen = request.FILES["photo"]
            new_user.save()
        else:
            new_user.save()
            
        #Envio de email de validación
        user = new_user.id
        html_content = "</br>Hola, por favor verifica tu email: <a href='http://localhost:8000/anuncios/validar-email?id_user={}&codigo={}'>Pincha aqui</a>".format(str(user), codigo)
        msg = EmailMultiAlternatives("Verifica tu email", "confirma", settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        context = {"validacion" : "Por favor revisa tu correo y verifica tu email para acceder a tu área de usuario"}
        return render(request, "login.html", context)

def validar_email(request):
    id_send = request.GET["id_user"]
    codigo_send =request.GET["codigo"]
    res = models.Usuario.objects.filter(id = id_send, codigo = codigo_send)
    #Compruebo si la sql da algún resultado
    if len(res)== 0:
        context = {"validacion": "La verificación de email ha fallado. Intentalo de nuevo"}
        return render(request, "login.html", context)
    else:
        user = res[0]
        user.email_validado = True
        user.save()
        context = {"validacion": "Gracias por verificar tu email!"}
        return render(request, "login.html", context)
    
def login(request):
    return render(request, "login.html")

def acceso_usuario(request):
    email_in = request.POST["email"].lower().strip()
    passwd_in = request.POST["passwd"]
    
    res = models.Usuario.objects.filter(email = email_in, contraseña = passwd_in, email_validado = True )   #comprobamos que el email y contraseña estén en la base de datos
    if len(res) == 0:
        context ={"error_login" : "El email o contraseña son erróneos o sin verificar"}
        return render(request,"login.html", context)
    else:
        usuario = res[0]
        request.session["id_usuario"] = usuario.id
        context = {"usuario_login" : usuario.usuario,
                   "imagen" : usuario.imagen}
        return render(request, "usuarios/area_usuario.html", context)
    
def buscar_anuncio(request):
    #mostrar la sql que lanza django para sacar los anuncios, es el código: 
    l = logging.getLogger('django.db.backends')    #recurso para mostrar cosas en pantalla
    l.setLevel(logging.DEBUG)                      #muestra sólo cuando estamos depurando
    l.addHandler(logging.StreamHandler())          #muestra sólo cuando estamos depurando
    
    #BUSCADOR
    categorias = models.Categoria.objects.order_by("id")  #cargo las categorias para incluirlas en el select.
    #Si ha puesto algo en el buscador: 
    titulo_buscador = ""
    if "titulo" in request.GET:
        titulo_buscador = request.GET["titulo"]
    #le damos los valores .prefetch_related('categoria', 'usuario') para que solo en una select, una las tablas, y no lance mil select
    res = models.Anuncio.objects.filter(titulo__contains = titulo_buscador).order_by("-id").prefetch_related('categoria', 'usuario')
    
    categoria_buscador = -1
    if "category" in request.GET and request.GET["category"] != "ninguna":
        categoria_buscador = request.GET["category"]
    if categoria_buscador != -1:    #en caso de que se haya seleccionado algo, hace el filtro sobre el res. 
        res = res.filter(categoria = categoria_buscador).prefetch_related('categoria')
    
    #PAGINACION (Para que salgan x anuncios por página)
    comienzo = 0 
    if "comienzo" in request.GET:
        comienzo = int(request.GET["comienzo"])
    siguiente = comienzo + 6
    anterior = comienzo - 6
    res = res[comienzo:comienzo+6]   #indico que solo coja de la bbdd los 6 primeros
    
    #sacamos el total de anuncios, para saber cuando tiene que parar de dar opción se siguiente
    total_anuncios = models.Anuncio.objects.count()
    
    context = { "anuncios": res,
               "categorias" : categorias,
               "titulo_bus": titulo_buscador,
               "categoria_bus": int(categoria_buscador),   #lo paso a entero para poder llamarlo luego en el html, ya que es el id.
               "siguiente": siguiente,
               "anterior" : anterior,
               "total_anuncios": total_anuncios }  #pasamos el valor para que vaya sumando
    
    return render(request, "encuentra.html", context)

def contacto_anuncios(request):
    id_user = request.GET["id_user"]
    user = models.Usuario.objects.get(pk = id_user)
    context = {"usuario": user,
               "title" : request.GET["titulo"]}
    return render(request, "contacto_anuncios.html", context)

def enviar_mensaje(request):
    subject = "Mensaje Anuncio: " + request.POST["subject"]
    message = request.POST["message"] + "\nContacto: " + request.POST["email"]
    email_from = settings.EMAIL_HOST_USER
    email_user = request.POST["email_user"]
    
    send_mail(subject, message, email_from, [email_user], fail_silently=False,)
    return render(request, "mensaje_enviado.html")