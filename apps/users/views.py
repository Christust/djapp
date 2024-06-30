from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
from django.views import generic, View
from . import models
from . import forms


# Create your views here.
class ListUsers(generic.ListView):
    template_name = "users/index.html"
    context_object_name = "users"
    model = models.User
    queryset = model.objects.filter(is_active=True)


class UpdateUser(generic.UpdateView):
    model = models.User
    form_class = forms.UserEditForm
    template_name = "users/edit.html"
    success_url = reverse_lazy("users:index")


class UpdateUserPassword(View):
    model = models.User
    form_class = forms.UserPasswordForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy("users:index")

    def get(self, request, pk):
        user = self.model.objects.filter(id=pk).first()
        form = self.form_class()
        print(self.form_class.as_table)
        return render(request, self.template_name, {"form": form, "object": user})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = self.model.objects.filter(id=pk).first()
            if user:
                user.set_password(form.cleaned_data.get("password"))
                user.save()
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            user = self.model.objects.filter(id=pk).first()
            return render(request, self.template_name, {"form": form, "object": user})


class CreateUser(generic.CreateView):
    model = models.User
    form_class = forms.UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:index")


class DeleteUser(generic.DeleteView):
    model = models.User
    success_url = reverse_lazy("users:index")


# Auth
class Login(generic.edit.FormView):
    template_name = "login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("index")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)
