from django.contrib import admin

# Register your models here.

from myapp.models import Genre


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)
