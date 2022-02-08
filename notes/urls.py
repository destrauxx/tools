from django.urls import path

from .views import (
    CreateCollectionView,
    CreateNoteView,
    ReadNotesView,
    UpdateNoteView,
    DeleteNoteView,
    add_note_to_collection,
    create_collection,
    DeleteCollection,
    mark_note_view,
    UpdateCollectionView
)

urlpatterns = [
    path('read/', ReadNotesView.as_view(), name='read_notes'),
    path('create/', CreateNoteView.as_view(), name='create_note'),
    path('delete/<int:pk>/', DeleteNoteView.as_view(), name='delete_note'),
    path('edit/<int:pk>/', UpdateNoteView.as_view(), name='edit_note'),
    path('collection/create', create_collection, name='create_collection'),
    path('collection/create_form/', CreateCollectionView.as_view(), name='create_collection_form'),
    path('collection/<pk>/delete/', DeleteCollection.as_view(), name='delete_collection'),
    path('collection/<pk>/edit/', UpdateCollectionView.as_view(), name='edit_collection'),
    path('collection/<collection_pk>/add_note/<note_pk>/', add_note_to_collection, name='add_note_to_collection'),
    path('mark/<pk>/', mark_note_view, name='mark_note'),
]