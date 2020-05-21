from django.db import models

# Create your models here.
#blank =True, null = True   para permitir que un campo sea nulo

class Categoria(models.Model):
    nombre_cat = models.CharField(max_length = 50)
    
    #indicamos función para mostrar los nombres en la zona de administración
    def __str__(self):
        return self.nombre_cat
    
class Usuario(models.Model):
    usuario = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 70, unique = True)
    contraseña = models.CharField(max_length = 20)
    imagen = models.FileField(upload_to="static/perfiles", null=True)
    email_validado = models.BooleanField(default = 0)
    codigo = models.CharField(max_length = 300)
    
    def __str__(self):
        return self.usuario
    
class Anuncio(models.Model):
    #indicamos los atributos de la clase, y le indicamos el tipo de campo y longitud. Django crea así las tablas en DB
    titulo = models.CharField(max_length = 70)
    precio = models.FloatField(default = 0)
    negociable = models.BooleanField()
    descripcion = models.CharField(max_length = 350)
    on_line = models.CharField(max_length = 2)
    fecha_modificacion = models.DateTimeField('fecha_modificacion')
    ip = models.CharField(max_length = 100)

    #asociamos el campo categoría a la clase, e indicamos que si se borra la categoria,se borran los anuncios aspciados
    categoria = models.ForeignKey(Categoria, on_delete= models.CASCADE)   
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE)
    
    foto = models.BooleanField(default= False)

    def __str__(self):
        return self.titulo + "  >>User: " + str(self.usuario)