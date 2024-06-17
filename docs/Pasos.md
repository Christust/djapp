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
python manage.py makemigrations <nombre de la app> --empty
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

# Plantillas

Las plantillas sera el html que se mostrara en el proyecto, estas pueden estar alojadas en cada apliación o en una carpeta especifica llamada templates en la raiz de nuestro proyecto. Sea donde sea que decidamos alojar las plantillas, estas no son mas que archivos html. Podemos por ejemplo crear la plantilla para la vista home

# Vistas

# Rutas

# Forms

# Archivos estaticos

