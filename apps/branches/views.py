from django.shortcuts import render
from apps.branches.forms import BranchForm

# Create your views here.
def Home(request):
    return render(request, "branch/index.html")

def CreateBranch(request):
    if request.method == "POST":
        branch_form = BranchForm