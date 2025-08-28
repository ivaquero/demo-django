from django.shortcuts import redirect, render

from .forms import ContactForm


# Create your views here.
def index(request):
    return render(request, "django_app/index.html")


def home_view(request):
    form = ContactForm()
    return render(request, "form_app/home.html", {"form": form})


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
