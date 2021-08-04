from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views.generic.edit import UpdateView

from .models import Note
from .forms import NoteForm


class NoteListView(ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    ordering = ['-date']
    #queryset = Note.objects.all().order_by('-date')
    paginate_by = 5


class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/note_detail.html'


class NoteUpdateView(UpdateView):
    model = Note
    fields = ['title', 'body']
    template_name_suffix = '_update_form'


class NoteView(View):
    def get(self, request):
        qs = Note.objects.all().order_by('-date')
        data = serializers.serialize('json', qs)
        return JsonResponse({'data': data}, safe=False)


def save_note_form(request, form, template):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

    data['html_form'] = render_to_string(
        template,
        {'form': form},
        request=request
    )
    return JsonResponse(data)


def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
    else:
        form = NoteForm()
    return save_note_form(request, form, 'notes/input_note.html')


def note_update(request, slug):
    note = get_object_or_404(Note, slug=slug)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
    else:
        form = NoteForm(instance=note)
    return save_note_form(request, form, 'notes/note_update_form.html')


def note_delete(request, slug):
    note = get_object_or_404(Note, slug=slug)
    data = dict()
    if request.method == "POST":
        note.delete()
        data['form_is_valid'] = True
    else:
        data["html_form"] = render_to_string(
            'notes/note_delete.html',
            {'note': note},
            request=request
        )

    return JsonResponse(data)
