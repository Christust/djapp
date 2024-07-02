from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .. import forms
from .. import models


# Create your views here.
# Item Requests
class ListItemRequests(generic.ListView):
    template_name = "item_requests/index.html"
    context_object_name = "item_requests"
    model = models.ItemRequest
    queryset = model.objects.filter(is_active=True)


class UpdateItemRequest(generic.UpdateView):
    model = models.ItemRequest
    form_class = forms.ItemRequestForm
    template_name = "item_requests/edit.html"
    success_url = reverse_lazy("stores:index_item_request")


class CreateItemRequest(generic.CreateView):
    model = models.ItemRequest
    form_class = forms.ItemRequestForm
    template_name = "item_requests/create.html"
    success_url = reverse_lazy("stores:index_item_request")


class DeleteItemRequest(generic.DeleteView):
    model = models.ItemRequest
    success_url = reverse_lazy("stores:index_item_request")
