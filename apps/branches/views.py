from django.shortcuts import render, redirect
from apps.branches.forms import BranchForm
from django.http import JsonResponse
from apps.branches.models import State, City

# Create your views here.
def Home(request):
    return render(request, "branches/index.html")

def CreateBranch(request):
    if request.method == "POST":
        branch_form = BranchForm(request.POST)
        if branch_form.is_valid():
            branch_form.save()
            return redirect("branches:index")
    else:
        branch_form = BranchForm()
    return render(request, "branches/create.html", {"branch_form": branch_form})

def load_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    return JsonResponse(list(states.values('id', 'name')), safe=False)

def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)
