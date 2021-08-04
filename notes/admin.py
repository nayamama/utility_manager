from django.contrib import admin

from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}


# Register your models here.
admin.site.register(Note)

