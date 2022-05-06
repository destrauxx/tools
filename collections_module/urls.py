from django.urls import path

from .views import (
    create_collection,
    CreateCollectionView,
    DeleteCollection,
    UpdateCollectionView,
    add_note_to_collection
)

urlpatterns = [
    path('collection/create', create_collection, name='create_collection'),
    path('collection/create_form/', CreateCollectionView.as_view(), name='create_collection_form'),
    path('collection/<pk>/delete/', DeleteCollection.as_view(), name='delete_collection'),
    path('collection/<pk>/edit/', UpdateCollectionView.as_view(), name='edit_collection'),
    path('collection/<collection_pk>/add_note/<note_pk>/', add_note_to_collection, name='add_note_to_collection'),
]