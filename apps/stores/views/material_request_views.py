from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from .. import forms
from .. import models


# Create your views here.
# Material Requests
class ListMaterialRequests(generic.ListView):
    template_name = "material_requests/index.html"
    context_object_name = "material_requests"
    model = models.MaterialRequest
    queryset = model.objects.filter(is_active=True)


class UpdateMaterialRequest(generic.UpdateView):
    model = models.MaterialRequest
    form_class = forms.MaterialRequestForm
    template_name = "material_requests/edit.html"
    success_url = reverse_lazy("stores:material_requests:index")


class CreateMaterialRequest(generic.CreateView):
    model = models.MaterialRequest
    form_class = forms.MaterialRequestForm
    template_name = "material_requests/create.html"
    success_url = "stores:material_requests:index"


class DeleteMaterialRequest(generic.DeleteView):
    model = models.MaterialRequest
    success_url = reverse_lazy("stores:material_requests:index")
