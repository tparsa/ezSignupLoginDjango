from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from myapp.forms import SignupForm, LoginForm
from myapp.models import Genre, Member
import logging

# Create your views here.

logger = logging.getLogger()


def hello_world(request):
    return HttpResponse("Hello World!")


def genres(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "Guest"
    errors = []
    if request.method == 'POST':
        genre_name = request.POST.get('name')
        if not genre_name:
            errors.append('name is a required field')
        else:
            Genre.objects.create(name=genre_name)
    all_genres = Genre.objects.all()
    return render(request, "genres.html", {
        "genres": all_genres,
        "errors": errors,
        "username": username,
    })


def get_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)

    if request.method == 'POST':
        request_type = request.POST['type']
        if request_type == 'delete':
            genre.delete()
            return HttpResponseRedirect(reverse('genres'))
        if request_type == 'update':
            genre_name = request.POST.get('name')
            genre.name = genre_name
            genre.save()
    return render(request, "genre.html", {
        "genre": genre
    })


def signup(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "signup.html", {
            "form": form,
        })
    else:
        form = SignupForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return render(request, "successful_signup.html", {
                    "username": form.cleaned_data['username'],
                })
            else:
                return render(request, "signup.html", {
                    "form": form
                })
        except Exception as e:
            logger.exception(e)
            return render(request, "signup.html", {
                "form": form
            })


def user_login(request):
    if request.user.is_authenticated:
        return genres(request)
    if request.method == "GET":
        return render(request, "login.html", {
            "errors": []
        })
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return render(request, "successful_logged_in.html", {
                "username": username,
            })
        else:
            return render(request, "login.html", {
                "errors": ["Invalid Username or Password"],
            })


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return genres(request)
