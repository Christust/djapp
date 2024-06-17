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