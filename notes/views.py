import math
from multiprocessing import context
from re import template
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import (
                                  CreateView,
                                  ListView,
                                  UpdateView,
                                  DeleteView,
                                    )
from .models import (
                     Note,
                     Collection,
                        )
from authenticate.models import UserInfo
from .forms import (
                    CreateNoteModelForm,
                    CreateCollectionModelForm,
                        )

class HomePageView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, 'index.html', {'profile': user})

class CreateNoteView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    form_class = CreateNoteModelForm
    template_name = 'notes/create_note.html'
    success_url = reverse_lazy('read_notes')
    success_message = "Your note has been successfully created!"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        context['user_info'] = get_object_or_404(UserInfo, user=self.request.user)
        return context

class UpdateNoteView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Note
    form_class = CreateNoteModelForm
    template_name = 'notes/edit_note.html'
    success_message = 'Your note was successfully updated!'
    success_url = reverse_lazy('read_notes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note'] = get_object_or_404(Note, pk=self.kwargs['pk'])
        context['user_info'] = get_object_or_404(UserInfo, user=self.request.user)
        return context

class DeleteNoteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_note.html'
    success_url = reverse_lazy('read_notes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.all()
        context['note'] = get_object_or_404(Note, pk=self.kwargs['pk'])
        context['user_info'] = get_object_or_404(UserInfo, user=self.request.user)
        context['pk'] = self.kwargs['pk']
        return context
        
class ReadNotesView(LoginRequiredMixin, ListView):
    template_name = 'notes/read_notes.html'
    paginate_by = 6
    context_object_name = 'notes'
        
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))

        selected_collection = int(request.GET.get('collection', 0))
        add_mode_collection = int(request.GET.get('add_mode_collection', 0)) # id коллекции, если пользователь добавляет к ней заметки

        if selected_collection:
            notes = Note.objects.filter(user=request.user, collection=selected_collection)
        elif add_mode_collection:
            notes = Note.objects.filter(user=request.user, collection=None)
        else:
            notes = Note.objects.filter(user=request.user)

        search_input = self.request.GET.get('search-input', '')
        if search_input:
            notes = Note.objects.filter(header__icontains=search_input)
            if not notes:
                messages.error(request, 'Notes Not Found!')
                return redirect('read_notes')


        collections = Collection.objects.filter(user=request.user)
        user_info = get_object_or_404(UserInfo, user=request.user)
        start_index = (page * self.paginate_by) - self.paginate_by
        end_index = page * self.paginate_by
        pages_count = math.ceil(len(notes) / self.paginate_by)

        if notes:
            notes_list = notes[start_index:end_index]
        else:
            notes_list = []

        return render(request, 'notes/read_notes.html', {
                                                         'notes_list': notes_list,
                                                         'collections': collections,
                                                         'current_page': page,
                                                         'next': page + 1,
                                                         'prev': page - 1,
                                                         'pages_count': pages_count,
                                                         'pages_count_list': range(1, pages_count+1),
                                                         'add_mode_collection': add_mode_collection,
                                                         'search_input': search_input,
                                                         'selected_collection': selected_collection,
                                                         'user_info': user_info,
                                                         })
    
class CreateCollectionView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CreateCollectionModelForm
    template_name = 'notes/collection_create_form.html'
    
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

    return render(request, 'notes/collection.html', {'collection': collection, 'user_info': user_info, 'current_page': page})

class DeleteCollection(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'notes/delete_collection.html'
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
    template_name = 'notes/edit_collection.html'
    success_message = "Your collection was successfully updated!"
    success_url = reverse_lazy('read_notes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['collection'] = get_object_or_404(Collection, pk=self.kwargs['pk'])
        context['user_info'] = get_object_or_404(UserInfo, user=self.request.user)
        return context

def mark_note_view(request, pk):
    note = get_object_or_404(Note, id=pk)
    note.is_important = not note.is_important
    note.save()

    return redirect('read_notes')
    
def add_note_to_collection(request, collection_pk, note_pk):
    collection = get_object_or_404(Collection, id=collection_pk)
    note = get_object_or_404(Note, id=note_pk)
    note.collection = collection
    note.save()

    return redirect(reverse('read_notes'))

# def change_custom(request):
#     user_info = get_object_or_404(UserInfo, user=request.user)
#     theme = request.GET.get('theme', '')
#     accent_color = request.GET.get('accent_color', '')

#     allowed_themes = ['dark', 'light']
#     allowed_accent_colors = ['red', 'green', 'light_blue', 'orange']
#     if theme in allowed_themes:
#         user_info.change_theme(theme)
#     if accent_color in allowed_accent_colors:
#         user_info.change_accent_color(accent_color)
#     user_info.save()

#     return redirect('homepage')

