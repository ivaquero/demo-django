from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View

from .forms import ContactForm, RegisterForm


# Create your views here.
def index(request):
    return render(request, "django_app/index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form": form})
    return None


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.POST.get("next") or request.GET.get("next") or "home"
            # return redirect(next_url)

        error_message = "Invalid Credentials"

    return render(request, "accounts/login.html", {"error_message": error_message})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("home")
    return render(request, "accounts/logout.html")


@login_required
def home_view(request):
    form = ContactForm()
    return render(request, "form_app/home.html", {"form": form})


class ProctectedView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get_login_url(self, request):
        return render(request, "registration/protected.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return redirect("contact-success")

    else:
        form = ContactForm()
    context = {"form": form}
    return render(request, "form_app/contact.html", context)


def contact_success_view(request):
    return render(request, "form_app/contact_success.html")
