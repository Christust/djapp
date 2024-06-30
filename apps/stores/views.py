from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from . import forms
from . import models


# Create your views here.
# Stores
class ListStores(generic.ListView):
    template_name = "stores/index.html"
    context_object_name = "stores"
    model = models.Store
    queryset = model.objects.filter(is_active=True)


class UpdateStore(generic.UpdateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = "stores/edit.html"
    success_url = reverse_lazy("stores:index_store")


class CreateStore(generic.CreateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = "stores/create.html"
    success_url = reverse_lazy("stores:index_store")


class DeleteStore(generic.DeleteView):
    model = models.Store
    success_url = reverse_lazy("stores:index_store")


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
    success_url = reverse_lazy("stores:index_item")


class CreateItem(generic.CreateView):
    model = models.Item
    form_class = forms.ItemForm
    template_name = "items/create.html"
    success_url = reverse_lazy("stores:index_item")


class DeleteItem(generic.DeleteView):
    model = models.Item
    success_url = reverse_lazy("stores:index_item")
    template_name = "items/item_confirm_delete.html"


# Stocks
class ListStocks(generic.ListView):
    template_name = "stocks/index.html"
    context_object_name = "stocks"
    model = models.Stock
    queryset = model.objects.filter(is_active=True)

    def get(self, request, pk_store):
        stocks = self.model.objects.filter(store_id=pk_store)
        store = models.Store.objects.filter(id=pk_store).first()
        context = {self.context_object_name: stocks, "store": store}
        return render(request, self.template_name, context)


class CreateStock(generic.CreateView):
    model = models.Stock
    form_class = forms.StockForm
    template_name = "stocks/create.html"

    def get(self, request, pk_store):
        context = {
            "form": self.form_class(
                initial={"store": pk_store, "store_hiden": pk_store}
            ),
            "store": {"id": pk_store},
        }
        return render(request, self.template_name, context)

    def post(self, request, pk_store):
        data = request.POST.copy()
        data["store"] = data["store_hiden"]
        form = self.form_class(data)
        if form.is_valid():
            form.save()
            return redirect(
                reverse_lazy(f"stores:stocks:index", kwargs={"pk_store": pk_store})
            )
        else:
            context = {
                "form": form,
                "store": {"id": pk_store},
            }
            return render(request, self.template_name, context)


class UpdateStock(generic.UpdateView):
    model = models.Stock
    form_class = forms.StockForm
    template_name = "stocks/edit.html"
    success_url = reverse_lazy("stores:index_stock")

    def get(self, request, pk_store, pk):
        stock = self.model.objects.filter(id=pk).first()
        context = {
            "form": self.form_class(instance=stock, store_hiden_initial=pk_store),
            "store": {"id": pk_store},
            "object": stock,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk_store, pk):
        stock = self.model.objects.filter(id=pk).first()
        data = request.POST.copy()
        data["store"] = data["store_hiden"]
        form = self.form_class(data, instance=stock)
        if form.is_valid():
            form.save()
            return redirect(
                reverse_lazy(f"stores:stocks:index", kwargs={"pk_store": pk_store})
            )
        else:
            context = {
                "form": form,
                "store": {"id": pk_store},
                "object": stock,
            }
            return render(request, self.template_name, context)


class DeleteStock(generic.DeleteView):
    model = models.Stock
    template_name = "stocks/stock_confirm_delete.html"
    success_url = "stores:stocks:index"

    def get(self, request, pk_store, pk):
        stock = self.model.objects.filter(id=pk).first()
        context = {
            "store": {"id": pk_store},
            "object": stock,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk_store, pk):
        stock = self.model.objects.filter(id=pk).first()

        if stock:
            stock.delete()
        return redirect(
            reverse_lazy(self.success_url, kwargs={"pk_store": pk_store})
        )


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
    success_url = reverse_lazy("stores:index_material_request")


class CreateMaterialRequest(generic.CreateView):
    model = models.MaterialRequest
    form_class = forms.MaterialRequestForm
    template_name = "material_requests/create.html"
    success_url = reverse_lazy("stores:index_material_request")


class DeleteMaterialRequest(generic.DeleteView):
    model = models.MaterialRequest
    success_url = reverse_lazy("stores:index_material_request")


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
