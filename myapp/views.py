from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from myapp.models import Genre


# Create your views here.


def hello_world(request):
    return HttpResponse("Hello World!")


def genres(request):
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
        "errors": errors
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
