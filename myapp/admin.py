from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from myapp.models import Genre, Member


class GenreAdmin(admin.ModelAdmin):
    pass


# class MemberAdmin(admin.ModelAdmin):
#     pass

admin.site.register(Member, UserAdmin)
admin.site.register(Genre, GenreAdmin)
# admin.site.register(Member, MemberAdmin)