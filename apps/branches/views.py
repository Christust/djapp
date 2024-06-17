from django.shortcuts import render
from django.http import HttpResponse
from apps.branches.forms import BranchForm

# Create your views here.
def Home(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def CreateBranch(request):
    if request.method == "POST":
        branch_form = BranchForm