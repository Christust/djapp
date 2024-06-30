from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import generic
from django.urls import reverse_lazy
from . import forms
from . import models

# Create your views here.
# def Home(request):a
#     return render(request, "branches/index.html")


class ListBranches(generic.ListView):
    template_name = "branches/index.html"
    context_object_name = "branches"
    model = models.Branch
    queryset = model.objects.filter(is_active=True)


# def listBranch(request):
#     branches = Branch.objects.all()
#     return render(request, "branches/index.html", {"branches": branches})


# def CreateBranch(request):
#     if request.method == "POST":
#         branch_form = BranchForm(request.POST)
#         if branch_form.is_valid():
#             branch_form.save()
#             return redirect("branches:index")
#     else:
#         branch_form = BranchForm()
#     return render(request, "branches/create.html", {"branch_form": branch_form})

# def editBranch(request, id):
#     branch = Branch.objects.filter(id=id).first()
#     if request.method == "GET":
#         branch_form = BranchForm(instance=branch)
#     else:
#         branch_form = BranchForm(request.POST, instance=branch)
#         if branch_form.is_valid():
#             branch_form.save()
#         return redirect("branches:index")
#     return render(request, "branches/create.html", {"branch_form": branch_form})


class UpdateBranch(generic.UpdateView):
    model = models.Branch
    form_class = forms.BranchForm
    template_name = "branches/edit.html"
    success_url = reverse_lazy("branches:index")


class CreateBranch(generic.CreateView):
    model = models.Branch
    form_class = forms.BranchForm
    template_name = "branches/create.html"
    success_url = reverse_lazy("branches:index")


class DeleteBranch(generic.DeleteView):
    model = models.Branch
    success_url = reverse_lazy("branches:index")


# def deleteBranch(request, id):
#     branch = Branch.objects.filter(id=id).first()
#     branch.delete()
#     return redirect("branches:index")


# Helpers


def load_states(request):
    country_id = request.GET.get("country_id")
    states = models.State.objects.filter(country_id=country_id).order_by("name")
    return JsonResponse(list(states.values("id", "name")), safe=False)


def load_cities(request):
    state_id = request.GET.get("state_id")
    cities = models.City.objects.filter(state_id=state_id).order_by("name")
    return JsonResponse(list(cities.values("id", "name")), safe=False)
