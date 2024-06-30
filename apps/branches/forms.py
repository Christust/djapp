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
