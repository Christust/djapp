from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .. import forms
from .. import models


# Create your views here.
# Stores
class ListStores(generic.ListView):
    template_name = "stores/index.html"
    context_object_name = "stores"
    model = models.Store
    queryset = model.objects.filter(is_active=True)


class CreateStore(generic.CreateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = "stores/create.html"
    success_url = reverse_lazy("stores:index")


class DetailStore(generic.DetailView):
    model = models.Store
    template_name = "stores/detail.html"


class UpdateStore(generic.UpdateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = "stores/edit.html"
    success_url = reverse_lazy("stores:index")


class DeleteStore(generic.DeleteView):
    model = models.Store
    success_url = reverse_lazy("stores:index")
