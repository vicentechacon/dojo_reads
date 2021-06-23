from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UsuarioManager(models.Manager):
    def validaciones_basicas(self, postData):
        errores = {}

        if len (postData['first_name'])<2:
            errores['first_name']= "Nombre debe tener al menos 2 caracteres"
        if len (postData['last_name'])<2:
            errores['last_name']= "Apellido debe tener al menos 2 caracteres"
        if len (postData['email']) <1:
            errores['email']= "Email es necesario"
        if len(postData['password']) < 5:
            errores['password']='Password debe tener al menos 5 caracteres'
        if postData['password'] != postData['confirmPassword']:
            errores['confirmacion'] = 'Contraseñas no coinciden'

        elif not EMAIL_REGEX.match(postData['email']):
            errores['email']= "Email is not valid"

        else:
            usuario = Usuario.objects.filter(email=postData['email'])
            if len(usuario)>0:
                errores['email_registrado'] = 'Email ya registrado, porfavor intentar otro email'

        return errores

    def login_validaciones(self, postData):
        login_errores = {}
        if 'email' in postData and len(postData['email']) == 0:
            login_errores['email'] = 'Email es necesario'
        elif not EMAIL_REGEX.match(postData['email']):
            login_errores['email']= "Email is not valid"
        else:
            email_existente = Usuario.objects.filter(email=postData['email'])
            if len(email_existente) == 0:
                login_errores['email_no_encontrado'] = 'Este correo no está registrado'
                return login_errores
            else:
                usuario = email_existente[0]
            if not bcrypt.checkpw(postData['password'].encode(), usuario.password.encode()):
                login_errores['password']='Password incorrecta'
            
        return login_errores


class Usuario(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsuarioManager()

    def __str__(self):
        return str(self.__dict__)
