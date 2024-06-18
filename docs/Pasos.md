# Pasos a seguir

Crear la carpeta del proyecto, y dentro de la misma crear un entorno virtual

```
virtualenv venv
```

Instalar Django

```
pip install django
```

Iniciar el proyecto en esa misma carpeta

```
django-admin startproject config .
```

Crear la carpeta apps, y dentro de ella ir creando las apps a utilizar.

Crear la carpeta templates y dentro de ella se crearan las plantillas a renderizar.

Para que nuestro proyecto tome las platillas de la carpeta templates necesitamos configurar en settings.py el array DIRS:

```
...
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
...
```

Si queremos cambiar el idioma de nuestro sistema podemos configurar la sección de lenguaje, cambiando la cadena de texto de "LANGUAGE_CODE" al sistema que deseemos, en este caso a español:

```
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "es" 

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
```

Cuando recien creamos un proyecto no necesitamos crear un modelo "User", Django ya crea uno por defecto, pero si nosotros deseamos crear nuestro propio modelo personalizado con atributos especificos podemos crear la aplicacion users y en su archivo models.py crear nuestro propio manager de usuarios (el atributo objects con el que hacemos consultas o creamos usuarios) y nuestro propio modelo usuario:

```
# Importamos models para crear nuestros atributos de nuestro modelo
from django.db import models

# Importamos AbstractBaseUser para crear un modelo personalizado de usuario casi desde 0
# Importamos BaseUserManager para crear un manager para nuestro modelo, el manager
# es el atributo llamado objects que gestiona las funciones create_user por ejemplo
# Importamos PermissionsMixin para heredar a nuestro usuario el mixin de permisos y grupos
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Importamos la clase HistoricalRecords, una app de terceros que lleva un historico de las
# acciones de nuestro modelo

# Create your models here.
class UserManager(BaseUserManager):
    # Función base que utilizaran nuestras funciones para crear usuarios normales o superusuario
    def _create_user(
        self,
        email: str,
        name: str,
        last_name: str,
        user_type: str,
        password: str | None,
        is_staff: bool,
        **extra_fields,
    ):
        """
        Función base que utilizaran nuestras funciones para crear usuarios normales o superusuario
        """

        # Instanciamos el modelo con los parametros recibidos
        user = self.model(
            email=email,
            name=name,
            last_name=last_name,
            user_type=user_type,
            is_staff=is_staff,
            **extra_fields,
        )

        # Encriptamos el parametro password y lo depositamos en el atributo password de
        # este usuario
        user.set_password(password)

        # Guardamos el usuario
        user.save(using=self.db)

    # Función para crear usuarios normales
    def create_user(
        self,
        email: str,
        name: str,
        last_name: str,
        user_type: str,
        password: str | None = None,
        **extra_fields,
    ):
        """
        Función para crear usuarios normales
        """

        # Con los parametros recibidos creamos un usuario normal llamando _create_user
        return self._create_user(
            email,
            name,
            last_name,
            user_type,
            password,
            False,
            **extra_fields,
        )

    # Función para crear superusuarios
    def create_superuser(
        self,
        email: str,
        name: str,
        last_name: str,
        user_type: str,
        password: str | None = None,
        **extra_fields,
    ):
        """
        Función para crear superusuarios
        """

        # Con los parametros recibidos creamos un superusuario llamando _create_user
        return self._create_user(
            email,
            name,
            last_name,
            user_type,
            password,
            True,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    # Enum de tipos de usuario
    class UserType(models.TextChoices):
        SUPER_ADMIN = "superadmin"
        ADMIN = "admin"
        COMMON = "common"

    # Atributo principal de nuestro modelo persoanlizado
    email = models.EmailField("Email", unique=True, max_length=100)

    # Atributos extra que personalizamos para nuestro modelo
    name = models.CharField("Name", max_length=100, blank=False, null=False)

    last_name = models.CharField("Lastname", max_length=100, blank=False, null=False)

    user_type = models.CharField(
        "User type", max_length=20, choices=UserType.choices, blank=False, null=False
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Atributos requeridos para nuestro mixin de permisos
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f"{self.name} {self.last_name}"

    @property
    def is_superuser(self):
        return self.user_type == self.UserType.SUPER_ADMIN

    # Atributo que sera nuestro manager
    objects = UserManager()

    # Clase Meta, declaramos aqui nuestro metadatos para el modelo
    class Meta:
        # Atributos para el nombre en singular y el nombre en plural
        verbose_name = "User"
        verbose_name_plural = "Users"

    # Atributos necesarios para un modelo de usuario

    # El atributo USERNAME_FIELD es para delcarar el atributo principal de la clase
    USERNAME_FIELD = "email"

    # El atributo REQUIRED_FIELDS se usa para declarar los atributos requeridos al crear un usuario
    REQUIRED_FIELDS = ["name", "last_name", "user_type"]

    # Función para declarar la llave natural del modelo, si hay relaciones uno a muchos o muchos
    # a muchos, en lugar de mostrar el id, mostrara lo que esta función nos retorne
    def natural_key(self):
        return self.email

    # Función para retornar un string al llamar una instancia de este modelo
    def __str__(self):
        return f"{self.full_name}"

```

Despues de esto debemos registrar en nuestro archivo settings.py la aplicacion y que este sera nuestro modelo users:

```
...
LOCAL_APPS = [
    ...
    "apps.users",
    ...
]
...

...
# CUSTOM

AUTH_USER_MODEL = "users.User"
...
```

Sea si usamos el usuario por defecto de django o creamos nuestro propio modelo, el siguiente paso sera correr las primeras migraciones:

```
python manage.py makemigrations
python manage.py migrate
```

# Aplicaciones

Para crear apliaciones debemos posicionarnos en la carpeta donde la crearemos y ejecutar:

```
django-admin startapp <nombre de la app>
```

Si creamos apps nuevas dentro de la carpeta apps debemos agregar el nombre de la carpeta al string que se declara dentro de app.py para cada apliacion:

```
from django.apps import AppConfig


class <Nombre de la app>Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.<nombre de la app>'
```

Para agregar la aplicación a nuestro settings.py agregamos el string declarado en el paso anterior al array de apps:

```
...
BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    ...
    "apps.<nombre de la app>",
    ...
]

THIRD_APPS = []

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS
...
```

# Modelos

Cuanto se crea una app podemos crear los modelos que se encargara de gestionar la app. Para ello en el archivo models.py se importa models de django.db, para crear nuestras clases las cuales representaran tablas en nuestra base de datos, esta clase debe de heredar de models.Model. Los atributos de las clases generadas en el archivo models.py seran los atributos de nuestra tabla.

```
from django.db import models


# Create your models here.
class <Nombre del modelo>(models.Model):
    attr1 = models.CharField("Atributo 1", max_length=50, blank=False, null=False)

    def natural_key(self):
        return self.attr1

    def __str__(self):
        return f"{self.attr1}"

    class Meta:
        verbose_name = <Nombre en singular>
        verbose_name_plural = <Nombre en plural>
```

Despues de crear los modelos necesarios procederemos a crear las migraciones:

```
python manage.py makemigrations
python manage.py migrate
```

Si se desea crear una migracion vacia para por ejemplo crear datos en una migracion ejecutamos:

```
python manage.py makemigrations <nombre de la app> --empty --name <nombre descriptivo de lo que se hara >
```

Posteriormente nos dirigimos a la migracion creada y agregamos la funcion que debe crear los registros y agregarla al array que ejecutara dicha función:

```
from django.db import migrations

def crear_registros(apps, schema_editor):
    MiModelo = apps.get_model('miapp', 'MiModelo')
    MiModelo.objects.create(campo1='valor1', campo2='valor2')
    MiModelo.objects.create(campo1='valor3', campo2='valor4')
    # Puedes agregar más registros aquí según sea necesario

class Migration(migrations.Migration):

    dependencies = [
        ('miapp', 'xxxx_migration_anterior'),
    ]

    operations = [
        migrations.RunPython(crear_registros),
    ]
```

## Relaciones

Las relaciones entre tablas describen el como se enlazan y se deben de comportar las tablas. El flujo de datos que se tiene y como se comportara el sistema.

### One to one

Si queremos declarar en un modelo que existe una relación de uno a uno debemos agregar el atributo al modelo de la siguiente forma:

```
<nombre del otro modelo> = models.OneToOneField(<Nombre del otro modelo>, on_delete=models.CASCADE, blank=False, null=False)
```

Este atributo solo se debe crear en uno de los dos modelos con la relacion uno a uno.

### One to many

Si queremos declarar un modelo con relacion uno a muchos debemos agregar la siguiente clausula a un atributo que represente al modelo que posee dichos modelos, para identificar quien debe llevar la relacion foranea debemos pensar que modelo pertenece a que modelo. Un ejemplo seria un modelo tiene muchos elementos de otro modelo, y dicho otro modelo pertenece al primer modelo. Entonces bajo esta logica quien debe llevar la clave foranea seria nuestro segundo modelo.

```
<nombre del otro modelo> = models.ForeignKey(<Nombre del otro modelo>, on_delete=models.CASCADE, blank=False, null=False)
```

### Many to many

La relación muchos a muchos puede estar en cualquier modelo que se desee, solo se debe declarar en uno de los dos modelos

```
<nombre del otro modelo> = models.ForeignKey(<Nombre del otro modelo>)
```

# Plantillas

Las plantillas sera el html que se mostrara en el proyecto, estas pueden estar alojadas en cada apliación o en una carpeta especifica llamada templates en la raiz de nuestro proyecto. Sea donde sea que decidamos alojar las plantillas, estas no son mas que archivos html que nuestros controladores renderizaran al final de cada función llamada por un endpoint.

# Vistas

Las vistas con los controladores de nuestro sistema, en los archivos views.py se encontraran las funciones que (enlzadas a una ruta) determinaran el comportamiento de nuestro sistema cuando consultamos o interactuamos con determinadas rutas.

Para agregar una funcion a nuestra vista basta con crear una funcion basica en python que reciba un parametro llamado "request", este parametro es obligatorio ya que representa la petición del cliente a ese endpoint en especifico, al final de una función de vista debemos retornar algo, para este caso de prueba usaremos la función "render", que viene importada por defecto en los archivos views.py creados automaticamente. La función render recibe dos parametros como minimo, el primero debe ser la peticion ("request") y el segundo el template que se debe mostrar una vez terminado el proceso que realiza el endpoint.

```
from django.shortcuts import render

# Create your views here.
def <nombre de la funcion>(request):
    return render(request, "<ruta de la carpeta>/<nombre del archivo>.html") 
```

En este caso en concreto se debe agregar la ruta de la carpeta contenedora, esto se hace en caso de que el archivo no se encuentre en la raiz de la carpeta "templates", si dentro de "templates" agregamos una subcarpeta con el nombre de la aplicación por ejemplo (para tener un mejor control de los archivos pertenecientes a la misma) debemos agregar a la cadena de texto de render la ruta del archivo como se muestra en el ejemplo.

Si nosotros queremos por ejemplo mandar datos, se dice que deseamos mandar un contexto, para ello debemos de crear un objeto en python (un diccionario) y mandarlo como tercer parametro, en este ejemplo estamos empleando un formulario:

```
def Create<Nombre del modelo>(request):
    if request.method == "POST":
        <nombre del modelo>_form = <Nombre del modelo>Form(request.POST)
        if <nombre del modelo>_form.is_valid():
            <nombre del modelo>_form.save()
            return redirect("<nombre del modelo en plural>:index")
    else:
        <nombre del modelo>_form = <Nombre del modelo>Form()
    return render(request, "<nombre del modelo>es/create.html", {"<nombre del modelo>_form": <nombre del modelo>_form})

```


# Rutas

Para gestionar las rutas o endpoints que nuestro sistema tendra debemos crear un archivo urls.py por cada aplicación que deseemos tenga rutas, este sera enlazado al archivo urls.py principal (el archivo urls.py que se crea por defecto al iniciar el proyecto ubicado en config o en la carpeta con el nombre del proyecto creada por defecto).

Para ello en el archivo urls.py principal del proyecto debemos agregar la funcion "include" y dentro del array de urlpatterns agregamos la ruta base de la aplicación y como segundo parametro la funcion "include" que recibira como parametro un string que indicara la ubicación del archivo urls de la apliación:

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    #path("<nombre de la aplicacion en plural (plurar por convención)>", include("apps.<nombre de la aplicación>.urls"))
]
```

Con esto estamos enlazando nuestro archivo urls.py de nuestra aplicación en cuestion a nuestro archivo urls.py del proyecto. Despues de esto debemos asegurarnos que minimamente nuestro archivo urls.py de la nuestra aplicación tenga la siguiente estructura:

```
from django.urls import path
from apps.<nombre de la aplicación> import views

urlpatterns = []
```


# Forms

Para iniciar debemos crear un archivo llamado forms.py en nuestra aplicación que querremos gestionar por medio de formularios automatizados de django. Para trabajar con los forms de django debemos crear una clase que representara un formulario, podemos crear una clase por cada modelo para gestionar su formulario general.

```
from django import forms
from apps.<nombre del modelo>.models import <Nombre del modelo>


class <Nombre del modelo>Form(forms.ModelForm):
    class Meta:
        model = <Nombre del modelo> # Modelo al cual pertenece este formulario
        fields = ["field1", "filed2", ...] # Este atributo representara los campos del modelo que se mostraran en el formulario.
```

Cuando heredamos de ModelForm heredamos los campos del modelo que incluyamos en la subclase Meta.

Al momento de utilizar el form en las plantillas debemos agregar una tag de django llamada csrf_token, el cual hara que nuestro form sea capaz de mandar los datos al backend de django, esto se hace para asegurarnos que los datos que estamos recibiendo son seguros y vienen de un origen de confianza. Un ejemplo seria asi:

```
<form method="POST">
    {% csrf_token %}
    {{ <nombre de la aplicacion>_form.as_p }}
    <button type="submit">Crear</button>
</form>
```

Para mandar un form este debe ser mandado como parte del contexto a una platilla, por defecto se manda un form vacio pero si se recibe la peticion por metodo "post" podremos llenar la data del form usando el request, verificar si es valido y guardar el registro:

```
def Create<Nombre del modelo>(request):
    if request.method == "POST":
        <nombre del modelo>_form = <Nombre del modelo>Form(request.POST)
        if <nombre del modelo>_form.is_valid():
            <nombre del modelo>_form.save()
            return redirect("<nombre del modelo en plural>:index")
    else:
        <nombre del modelo>_form = <Nombre del modelo>Form()
    return render(request, "<nombre del modelo>es/create.html", {"<nombre del modelo>_form": <nombre del modelo>_form})

```

# Archivos estaticos

# Admin

Si queremos registrar alguna aplicación al sitio de administración de Django, tenemos que modificar el archivo admin.py de la aplicación a registrar:

```
from django.contrib import admin
from apps.<nombre de la aplicación>.models import <Nombre del modelo>

# Register your models here.
admin.site.register(<Nombre del modelo>)
```

Agregando esto podemos ver nuestro modelo y sus registros en la pagina de aministración
