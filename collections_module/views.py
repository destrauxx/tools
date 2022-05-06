from django.shortcuts import render, redirect
from .models import Collection
from .forms import CreateCollectionModelForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from authenticate.models import UserInfo
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
)
from notes.models import Note

# Create your views here.
class CreateCollectionView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CreateCollectionModelForm
    template_name = 'collections/collection_create_form.html'
    success_url = reverse_lazy('read_notes')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['user_info'] = get_object_or_404(UserInfo, user=self.request.user)
        return context

def create_collection(request):
    form = CreateCollectionModelForm(request.POST or None)
    page = int(request.GET.get('page', 1))
    user_info = get_object_or_404(UserInfo, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()

    return render(request, 'collections/collection.html', {'collection': collection, 'user_info': user_info, 'current_page': page})

class DeleteCollection(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'collections/delete_collection.html'
    success_url = reverse_lazy('read_notes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Collections'] = Collection.objects.all()
        context['collection'] = get_object_or_404(Collection, pk=self.kwargs['pk'])
        context['user_info'] = get_object_or_404(UserInfo, user=self.request.user)
        context['pk'] = self.kwargs['pk']
        return context

class UpdateCollectionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Collection
    form_class = CreateCollectionModelForm
    template_name = 'collections/edit_collection.html'
    success_message = "Your collection was successfully updated!"
    success_url = reverse_lazy('read_notes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['collection'] = get_object_or_404(Collection, pk=self.kwargs['pk'])
        context['user_info'] = get_object_or_404(UserInfo, user=self.request.user)
        return context

def add_note_to_collection(request, collection_pk, note_pk):
    collection = get_object_or_404(Collection, id=collection_pk)
    note = get_object_or_404(Note, id=note_pk)
    note.collection = collection
    note.save()

    return redirect(reverse('read_notes'))
