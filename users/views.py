from django.views.generic import CreateView

from .forms import CreationForm
from django.shortcuts import render


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "signup.html"


def about_author(request):
    return render(request, "about_author.html")


def about_spec(request):
    return render(request, "about_spec.html")
