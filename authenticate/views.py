from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate as auth_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from authenticate import forms
from consts import MessagesConsts


@require_http_methods(["GET", "POST"])
def login(request):
    if not request.user.is_authenticated:
        form = forms.LoginForm(data=request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                username = request.POST["username"]
                password = request.POST["password"]

                user = auth_user(request, username=username, password=password)

                if user is not None:
                    auth_login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)

                messages.add_message(request, messages.ERROR, MessagesConsts.LOGIN_ERROR)

        return render(request, "login.html", {"form": form})

    else:
        return redirect(settings.LOGIN_REDIRECT_URL)


@login_required
@require_http_methods(["GET"])
def logout(request):
    auth_logout(request)

    return redirect(settings.LOGIN_REDIRECT_URL)
