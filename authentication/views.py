from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def register_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(username=email, email=email, password=password)

        login(request, user)

        return redirect("/") # reverse("dashboard")

    else:
        return render(request, "authentication/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("/") # reverse("dashboard")
        else:
            messages.add_message(request, messages.ERROR, "Incorrect credentials.")
            return redirect(reverse("login_view"))

    else:
        return render(request, "authentication/login.html")

@login_required(login_url="/auth/login")
def logout_view(request):
    logout(request)
    return redirect("/")
