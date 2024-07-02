Descripcion

El proyecto es un sistema que gestiona Branches (Sucursales), Stores (Almacenes), Stocks, Items (Pueden ser productos o herramientas), MaterialRequests (Peticiones de material para ser usado y posiblemente regresado al almacen si el Item no es un consumible), MaterialRequirement (Requisiciones de material para reabastecer el almacen), ItemRequests (La cantidad de items a pedir en una peticion de material) y ItemRequirements (La cantidad de items a requerir para reabastecer el almacen)

La estructura es la siguiente:

```
- apps
    - base
    - branches
    - stores
    - users
- config
    __init__.py
    asgi.py
    settings.py
    etc...
- static
- templates
    - branches
        branch_confirm_delete.html
        create.html
        edit.html
        index.html
    - users
        create.html
        etc...
    - stores
    - stockes
    - items
    - material_requests
    - material_requirements
    - item_requests
    - item_requirements
    footer.html
    index.html
    login.html
    navbar.html
```

La carpeta apps contiene las apps del proyecto entonces puedes asumir que en dichas carpetas la estructura de sus archivos son la de las apps normales de un proyecto django, la app base es especial esa solo sirve para darle a los modelos que hereden del modelo 'Base' creado en esta app contengan atributos comunes.

La carpeta config es la carpeta que el comando djangostartproject te genera pero yo la nombre config usando el comando asi:

```
djangostartproject config .
```

Esta carpeta contiene lo que generalmente contiene la carpeta con los archvios settings y urls de todo el proyecto.

-----------------------------
Apps

- Base

models.py:

```
from django.db import models


# Create your models here.
class Base(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField("Status", default=True)
    created_at = models.DateField("Creation date", auto_now_add=True)
    modified_at = models.DateField("Modification date", auto_now=True)
    deleted_at = models.DateField("Deletion date", null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"
```

- Branches

models.py:
```
from django.db import models
from apps.base.models import Base


# Create your models here.
class Country(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class State(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False, null=False)

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"

class City(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=False, null=False)

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

class Branch(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=False, null=False
    )

    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=False, null=False)

    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, null=False)

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

```

forms.py:

```
from django import forms
from . import models


class BranchForm(forms.ModelForm):
    class Meta:
        model = models.Branch
        fields = ["name", "country", "state", "city"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "country": forms.Select(attrs={"class": "form-control mb-3"}),
            "state": forms.Select(attrs={"class": "form-control mb-3"}),
            "city": forms.Select(attrs={"class": "form-control mb-3"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country"].queryset = models.Country.objects.all()
        self.fields["state"].queryset = models.State.objects.none()
        self.fields["city"].queryset = models.City.objects.none()

        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["state"].queryset = models.State.objects.filter(
                    country_id=country_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["state"].queryset = self.instance.country.state_set

        if "state" in self.data:
            try:
                state_id = int(self.data.get("state"))
                self.fields["city"].queryset = models.City.objects.filter(
                    state_id=state_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["city"].queryset = self.instance.state.city_set

```

views.py:

```
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import generic
from django.urls import reverse_lazy
from . import forms
from . import models

# Create your views here.
# def Home(request):a
#     return render(request, "branches/index.html")


class ListBranches(generic.ListView):
    template_name = "branches/index.html"
    context_object_name = "branches"
    model = models.Branch
    queryset = model.objects.filter(is_active=True)


# def listBranch(request):
#     branches = Branch.objects.all()
#     return render(request, "branches/index.html", {"branches": branches})


# def CreateBranch(request):
#     if request.method == "POST":
#         branch_form = BranchForm(request.POST)
#         if branch_form.is_valid():
#             branch_form.save()
#             return redirect("branches:index")
#     else:
#         branch_form = BranchForm()
#     return render(request, "branches/create.html", {"branch_form": branch_form})

# def editBranch(request, id):
#     branch = Branch.objects.filter(id=id).first()
#     if request.method == "GET":
#         branch_form = BranchForm(instance=branch)
#     else:
#         branch_form = BranchForm(request.POST, instance=branch)
#         if branch_form.is_valid():
#             branch_form.save()
#         return redirect("branches:index")
#     return render(request, "branches/create.html", {"branch_form": branch_form})


class UpdateBranch(generic.UpdateView):
    model = models.Branch
    form_class = forms.BranchForm
    template_name = "branches/edit.html"
    success_url = reverse_lazy("branches:index")


class CreateBranch(generic.CreateView):
    model = models.Branch
    form_class = forms.BranchForm
    template_name = "branches/create.html"
    success_url = reverse_lazy("branches:index")


class DeleteBranch(generic.DeleteView):
    model = models.Branch
    success_url = reverse_lazy("branches:index")


# def deleteBranch(request, id):
#     branch = Branch.objects.filter(id=id).first()
#     branch.delete()
#     return redirect("branches:index")


# Helpers


def load_states(request):
    country_id = request.GET.get("country_id")
    states = models.State.objects.filter(country_id=country_id).order_by("name")
    return JsonResponse(list(states.values("id", "name")), safe=False)


def load_cities(request):
    state_id = request.GET.get("state_id")
    cities = models.City.objects.filter(state_id=state_id).order_by("name")
    return JsonResponse(list(cities.values("id", "name")), safe=False)

```

urls.py:

```
from django.urls import path
from . import views

app_name = "branches"
urlpatterns = [
    path("", views.ListBranches.as_view(), name="index"),
    path("create/", views.CreateBranch.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateBranch.as_view(), name="update"),
    path("delete/<int:pk>", views.DeleteBranch.as_view(), name="delete"),
    # Helpers
    path("ajax/load_states/", views.load_states, name="ajax_load_states"),
    path("ajax/load_cities/", views.load_cities, name="ajax_load_cities"),
]

```

- Stores

Nota - Esta app la decidi dividir con carpetas, ya que los modelos que maneja son muchos decidi hacer una carpeta para las views y una para las urls y ahi colocar las views y urls de cada modelo administrado por esta app con la siguiente regla:

```
# Para las views
nombre_del_modelo_views.py

# Para las urls
nombre_del_modelo_urls.py
```

Ejemplos:
```
# Urls
item_urls.py
item_request_urls.py

# Views
item_views.py
item_request_views.py
```

En la carpeta urls de esta app colque un archivo llamado app_urls.py el cual sera aquel que importe todas las demas urls de ese mismo archivo y las pienso acomodar en la variable urlpatterns para que este sea el unico archivo importando desde la carpeta config en el archivo urls.py general del proyecto.

forms.py:

```
from django import forms
from . import models


class StoreForm(forms.ModelForm):
    class Meta:
        model = models.Store
        exclude = ["is_active", "created_at", "modified_at", "deleted_at"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "branch": forms.Select(attrs={"class": "form-control mb-3"}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        exclude = ["is_active", "created_at", "modified_at", "deleted_at"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "brand": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "barcode": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "consumable": forms.CheckboxInput(attrs={"class": "form-check-input mb-3"}),
            "units": forms.Select(attrs={"class": "form-control mb-3"}),
        }


class StockWithStoreForm(forms.ModelForm):
    store_hiden = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        store_hiden_initial = kwargs.pop(
            "store_hiden_initial", None
        )  # Extrae el valor del campo adicional si se proporciona
        super(StockForm, self).__init__(*args, **kwargs)
        if store_hiden_initial:
            self.fields["store_hiden"].initial = (
                store_hiden_initial  # Establece el valor inicial del campo adicional
            )

    class Meta:
        model = models.Stock
        exclude = ["is_active", "created_at", "modified_at", "deleted_at"]
        widgets = {
            "item": forms.Select(attrs={"class": "form-control mb-3"}),
            "store": forms.Select(
                attrs={"class": "form-control mb-3", "disabled": True}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese una cantidad",
                }
            ),
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = models.Stock
        exclude = ["is_active", "created_at", "modified_at", "deleted_at"]
        widgets = {
            "item": forms.Select(attrs={"class": "form-control mb-3"}),
            "store": forms.Select(attrs={"class": "form-control mb-3"}),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese una cantidad",
                }
            ),
        }


class MaterialRequestForm(forms.ModelForm):
    store_hiden = forms.IntegerField(widget=forms.HiddenInput())
    user_hiden = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        store_hiden_initial = kwargs.pop(
            "store_hiden_initial", None
        )  # Extrae el valor del campo adicional si se proporciona
        user_hiden_initial = kwargs.pop("user_hiden_initial", None)
        super(MaterialRequestForm, self).__init__(*args, **kwargs)
        if store_hiden_initial:
            self.fields["store_hiden"].initial = (
                store_hiden_initial  # Establece el valor inicial del campo adicional
            )

        if user_hiden_initial:
            self.fields["user_hiden"].initial = (
                user_hiden_initial  # Establece el valor inicial del campo adicional
            )

    class Meta:
        model = models.MaterialRequest
        exclude = ["is_active", "created_at", "modified_at", "deleted_at"]
        widgets = {
            "finished": forms.CheckboxInput(
                attrs={
                    "class": "mb-3",
                    "placeholder": "Finalizado",
                }
            ),
            "store": forms.Select(attrs={"class": "form-control mb-3"}),
            "user": forms.Select(attrs={"class": "form-control mb-3"}),
        }


class MaterialRequirementForm(forms.ModelForm):
    class Meta:
        model = models.MaterialRequirement
        exclude = ["is_active", "created_at", "modified_at", "deleted_at"]
        widgets = {
            "finished": forms.CheckboxInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Finalizado",
                }
            ),
            "store": forms.Select(attrs={"class": "form-control mb-3"}),
            "user": forms.Select(attrs={"class": "form-control mb-3"}),
        }


class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = models.ItemRequest
        exclude = ["is_active", "created_at", "modified_at", "deleted_at"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese una cantidad",
                }
            ),
            "amount_returned": forms.NumberInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese una cantidad",
                }
            ),
            "item": forms.Select(attrs={"class": "form-control mb-3"}),
            "material_request": forms.Select(attrs={"class": "form-control mb-3"}),
        }


class ItemRequirementForm(forms.ModelForm):
    class Meta:
        model = models.ItemRequirement
        exclude = ["is_active", "created_at", "modified_at", "deleted_at"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese una cantidad",
                }
            ),
            "item": forms.Select(attrs={"class": "form-control mb-3"}),
            "material_requirement": forms.Select(attrs={"class": "form-control mb-3"}),
        }

```

models.py:

```
from django.db import models
from apps.base.models import Base
from apps.branches.models import Branch
from apps.users.models import User


# Create your models here.
class Store(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=False, null=False
    )

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"


class Item(Base):
    class Units(models.TextChoices):
        UNITS = "units"
        METERS = "meters"
        LITERS = "liters"

    name = models.CharField("Name", max_length=50, blank=False, null=False)
    description = models.CharField(
        "Description", max_length=50, blank=False, null=False
    )
    brand = models.CharField("Brand", max_length=50, blank=False, null=False)
    barcode = models.CharField("Barcode", max_length=50, blank=False, null=False)
    consumable = models.BooleanField("Consumable", default=False)
    units = models.CharField(
        "Units", max_length=20, choices=Units.choices, blank=False, null=False
    )

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Stock(Base):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=False)
    amount = models.IntegerField("Amount", blank=False, null=False)

    def natural_key(self):
        return self.item

    def __str__(self):
        return f"{self.store} - {self.item}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

        # Unico item por store
        unique_together = ('store', 'item')


class MaterialRequest(Base):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, blank=False, null=False, default=1
    )
    finished = models.BooleanField("Finished", default=False)

    def natural_key(self):
        return self.store

    def __str__(self):
        return f"{self.store}"

    class Meta:
        verbose_name = "Material Request"
        verbose_name_plural = "Material Requests"


class MaterialRequirement(Base):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, blank=False, null=False, default=1
    )
    finished = models.BooleanField("Finished", default=False)

    def natural_key(self):
        return self.store

    def __str__(self):
        return f"{self.store}"

    class Meta:
        verbose_name = "Material Requirement"
        verbose_name_plural = "Material Requirements"


class ItemRequest(Base):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    material_request = models.ForeignKey(
        MaterialRequest, on_delete=models.CASCADE, blank=False, null=False
    )
    amount = models.IntegerField("Amount", blank=False, null=False)
    amount_returned = models.IntegerField(
        "Amount returned", blank=False, null=False, default=0
    )

    def natural_key(self):
        return self.item

    def __str__(self):
        return f"{self.item}"

    class Meta:
        verbose_name = "Item Request"
        verbose_name_plural = "Item Requests"


class ItemRequirement(Base):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    material_requirement = models.ForeignKey(
        MaterialRequirement, on_delete=models.CASCADE, blank=False, null=False
    )
    amount = models.IntegerField("Amount", blank=False, null=False)

    def natural_key(self):
        return self.item

    def __str__(self):
        return f"{self.item}"

    class Meta:
        verbose_name = "Item Requirement"
        verbose_name_plural = "Item Requirements"

```

- Users

forms.py:

```
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from . import models


class LoginForm(AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Nombre de usuario"
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["placeholder"] = "Contraseña del usuario"


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["email", "name", "last_name", "user_type", "password"]
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un email",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un apellido",
                }
            ),
            "user_type": forms.Select(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un tipo de usuario",
                }
            ),
            "password": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un password",
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["email", "name", "last_name", "user_type"]
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un email",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un nombre",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un apellido",
                }
            ),
            "user_type": forms.Select(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Ingrese un tipo de usuario",
                }
            ),
        }


class UserPasswordForm(forms.Form):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Ingrese la contraseña",
            }
        ),
    )
    password_confirmation = forms.CharField(
        label="Confirmación de contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Ingrese de nuevo la contraseña",
            }
        ),
    )

    def clean_password_confirmation(self):
        password_confirmation_clean = self.cleaned_data.get("password_confirmation")
        password_clean = self.cleaned_data.get("password")
        if password_confirmation_clean is not password_clean:
            raise ValidationError("La confirmación de contraseña debe ser igual")
        return password_confirmation_clean

```

models.py:

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

views.py:

```
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
from django.views import generic, View
from . import models
from . import forms


# Create your views here.
class ListUsers(generic.ListView):
    template_name = "users/index.html"
    context_object_name = "users"
    model = models.User
    queryset = model.objects.filter(is_active=True)


class UpdateUser(generic.UpdateView):
    model = models.User
    form_class = forms.UserEditForm
    template_name = "users/edit.html"
    success_url = reverse_lazy("users:index")


class UpdateUserPassword(View):
    model = models.User
    form_class = forms.UserPasswordForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy("users:index")

    def get(self, request, pk):
        user = self.model.objects.filter(id=pk).first()
        form = self.form_class()
        print(self.form_class.as_table)
        return render(request, self.template_name, {"form": form, "object": user})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = self.model.objects.filter(id=pk).first()
            if user:
                user.set_password(form.cleaned_data.get("password"))
                user.save()
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            user = self.model.objects.filter(id=pk).first()
            return render(request, self.template_name, {"form": form, "object": user})


class CreateUser(generic.CreateView):
    model = models.User
    form_class = forms.UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:index")


class DeleteUser(generic.DeleteView):
    model = models.User
    success_url = reverse_lazy("users:index")


# Auth
class Login(generic.edit.FormView):
    template_name = "login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("index")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

```

urls.py:

```
from django.urls import path
from django.contrib.auth.views import logout_then_login
from . import views

app_name = "users"
urlpatterns = [
    path("", views.ListUsers.as_view(), name="index"),
    path("create/", views.CreateUser.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateUser.as_view(), name="update"),
    path("delete/<int:pk>", views.DeleteUser.as_view(), name="delete"),
    # Auth
    path("login/", views.Login.as_view(template_name="login.html"), name="login"),
    path("logout/", logout_then_login, name="logout"),
    path(
        "change_password/<int:pk>",
        views.UpdateUserPassword.as_view(),
        name="change_password",
    ),
]

```