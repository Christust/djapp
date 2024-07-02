from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .. import forms
from .. import models


# Create your views here.
# Material Requirements
class ListMaterialRequirements(generic.ListView):
    template_name = "material_requirements/index.html"
    context_object_name = "material_requirements"
    model = models.MaterialRequirement
    queryset = model.objects.filter(is_active=True)


class UpdateMaterialRequirement(generic.UpdateView):
    model = models.MaterialRequirement
    form_class = forms.MaterialRequirementForm
    template_name = "material_requirements/edit.html"
    success_url = reverse_lazy("stores:index_material_requirement")


class CreateMaterialRequirement(generic.CreateView):
    model = models.MaterialRequirement
    form_class = forms.MaterialRequirementForm
    template_name = "material_requirements/create.html"
    success_url = reverse_lazy("stores:index_material_requirement")


class DeleteMaterialRequirement(generic.DeleteView):
    model = models.MaterialRequirement
    success_url = reverse_lazy("stores:index_material_requirement")
