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

ItemRequestFormSet = forms.inlineformset_factory(
    parent_model=models.MaterialRequest,
    model=models.ItemRequest,
    form=ItemRequestForm,
    fields=('item', 'amount'),
    extra=1,  # Número inicial de formularios de ItemRequest mostrados
    can_delete=False
)

