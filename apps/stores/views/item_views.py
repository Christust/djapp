from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .. import forms
from .. import models


# Create your views here.
# Items
class ListItems(generic.ListView):
    template_name = "items/index.html"
    context_object_name = "items"
    model = models.Item
    queryset = model.objects.filter(is_active=True)


class UpdateItem(generic.UpdateView):
    model = models.Item
    form_class = forms.ItemForm
    template_name = "items/edit.html"
    success_url = reverse_lazy("stores:items:index")


class CreateItem(generic.CreateView):
    model = models.Item
    form_class = forms.ItemForm
    template_name = "items/create.html"
    success_url = reverse_lazy("stores:items:index")


class DeleteItem(generic.DeleteView):
    model = models.Item
    success_url = reverse_lazy("stores:items:index")
    template_name = "items/item_confirm_delete.html"
