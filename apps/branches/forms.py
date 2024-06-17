from django import forms
from apps.branches.models import Branch


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "country", "state", "city"]
