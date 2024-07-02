from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .. import forms
from .. import models


# Create your views here.
# # Stocks


class ListStocks(generic.ListView):
    template_name = "stocks/index.html"
    context_object_name = "stocks"
    model = models.Stock
    queryset = model.objects.filter(is_active=True)


class CreateStock(generic.CreateView):
    model = models.Stock
    form_class = forms.StockForm
    template_name = "stocks/create.html"
    success_url = reverse_lazy("stores:stocks:index")


class UpdateStock(generic.UpdateView):
    model = models.Stock
    form_class = forms.StockForm
    template_name = "stocks/edit.html"
    success_url = reverse_lazy("stores:stocks:index")


class DeleteStock(generic.DeleteView):
    model = models.Stock
    template_name = "stocks/stock_confirm_delete.html"
    success_url = reverse_lazy("stores:stocks:index")


# Custom
class ListStocks2(generic.ListView):
    template_name = "stocks/index.html"
    context_object_name = "stocks"
    model = models.Stock
    queryset = model.objects.filter(is_active=True)

    def get(self, request, pk_store):
        stocks = self.model.objects.filter(store_id=pk_store)
        store = models.Store.objects.filter(id=pk_store).first()
        context = {self.context_object_name: stocks, "store": store}
        return render(request, self.template_name, context)


class CreateStock2(generic.CreateView):
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


class UpdateStock2(generic.UpdateView):
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


class DeleteStock2(generic.DeleteView):
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
        return redirect(reverse_lazy(self.success_url, kwargs={"pk_store": pk_store}))
