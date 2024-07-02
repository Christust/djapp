from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
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

    def get(self, request, pk_store):
        material_requests = self.model.objects.filter(store_id=pk_store)
        store = models.Store.objects.filter(id=pk_store).first()
        context = {self.context_object_name: material_requests, "store": store}
        return render(request, self.template_name, context)


class UpdateMaterialRequest(generic.UpdateView):
    model = models.MaterialRequest
    form_class = forms.MaterialRequestForm
    template_name = "material_requests/edit.html"
    success_url = reverse_lazy("stores:index_material_request")


class CreateMaterialRequest(generic.CreateView):
    model = models.MaterialRequest
    form_class = forms.MaterialRequestForm
    template_name = "material_requests/create.html"
    success_url = "stores:material_requests:index"

    def get(self, request, pk_store):
        context = {
            "form": self.form_class(
                initial={
                    "store": pk_store,
                    "store_hiden": pk_store,
                    "user": request.user.id,
                    "user_hiden": request.user.id,
                }
            ),
            "store": {"id": pk_store},
        }
        return render(request, self.template_name, context)

    def post(self, request, pk_store):
        data = request.POST.copy()
        data["store"] = data["store_hiden"]
        data["user"] = data["user_hiden"]
        form = self.form_class(data)
        if form.is_valid():
            form.save()
            return redirect(
                reverse_lazy(self.success_url, kwargs={"pk_store": pk_store})
            )
        else:
            context = {
                "form": form,
                "store": {"id": pk_store},
            }
            return render(request, self.template_name, context)


class DeleteMaterialRequest(generic.DeleteView):
    model = models.MaterialRequest
    success_url = reverse_lazy("stores:index_material_request")

