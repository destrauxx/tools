import math
from multiprocessing import context

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
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
from .models import Note
from collections_module.models import Collection
from authenticate.models import UserInfo
from .forms import CreateNoteModelForm
from .models import Note

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
        s = False
        notes_count = Note.objects.all().count()
        if search_input:
            s = True
            notes = Note.objects.filter(header__icontains=search_input)
            notes_count = Note.objects.filter(header__icontains=search_input).all().count()
            if not notes:
                s = False
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
                                                         'notes_count': notes_count,
                                                         's': s
                                                         })
    

def mark_note_view(request, pk):
    note = get_object_or_404(Note, id=pk)
    note.is_important = not note.is_important
    note.save()

    return redirect('read_notes')