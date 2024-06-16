from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    context = {"prueba": "prueba textual"}
    return render(request, "users/index.html", context)


def login(request):
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        #redirect
    else:
        return "error"
        #return error

def logout(request):
    logout(request)
    #return login page