from django.shortcuts import render
from .models import Task
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks' 
    # objectの名前変更

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        #ログインしているユーザーが作成した投稿だけを見る

        searchInputText = self.request.GET.get('search') or""
        if searchInputText:
            context['tasks'] = context['tasks'].filter(title__startswith=searchInputText)
        #検索機能

        context['search'] = searchInputText
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task' 

class TaskCreate(LoginRequiredMixin, CreateView):
    model  = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    #ログインしているユーザーだけが投稿できるようにする
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model  = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'todoapp/delete.html'
    context_object_name = 'task' 

class TaskLogin(LoginView):
    fields = '__all__'
    template_name = 'todoapp/login.html'

    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskLogout(LogoutView):
    fields = '__all__'
    template_name = 'todoapp/login.html'

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterTodo(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    #新規登録の保存