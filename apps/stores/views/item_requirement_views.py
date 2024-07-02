from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .. import forms
from .. import models


# Create your views here.
# Item Requirements
class ListItemRequirements(generic.ListView):
    template_name = "item_requirements/index.html"
    context_object_name = "item_requirements"
    model = models.ItemRequirement
    queryset = model.objects.filter(is_active=True)


class UpdateItemRequirement(generic.UpdateView):
    model = models.ItemRequirement
    form_class = forms.ItemRequirementForm
    template_name = "item_requirements/edit.html"
    success_url = reverse_lazy("stores:index_item_requirement")


class CreateItemRequirement(generic.CreateView):
    model = models.ItemRequirement
    form_class = forms.ItemRequirementForm
    template_name = "item_requirements/create.html"
    success_url = reverse_lazy("stores:index_item_requirement")


class DeleteItemRequirement(generic.DeleteView):
    model = models.ItemRequirement
    success_url = reverse_lazy("stores:index_item_requirement")
