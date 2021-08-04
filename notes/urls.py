from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('fill/', views.note_create, name='new_note'),
    path('<slug:slug>/update/', views.note_update, name='update_note'),
    path('<slug:slug>', views.NoteDetailView.as_view(), name='note_detail'),
    path('<slug:slug>/delete/', views.note_delete, name='note_delete'),
    path('data-json/', views.NoteView.as_view(), name='data-json'),
    path('', views.NoteListView.as_view(), name='note_list'),
]