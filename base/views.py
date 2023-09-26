from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.

class TaskList(LoginRequiredMixin, ListView):
    model = Task 
    context_object_name= 'tasks'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']= context['tasks'].filter(complete= False).count()    

        #fetching the search get request input which is the name of the form or an empty string
        search_input= self.request.GET.get('search-area')   
        #if there exsits a search input then filter it by the title 
        if search_input:
            context['tasks']= context['tasks'].filter(title__startswith= search_input)
        #whatever we pass, pass it to the template 
        context['search_input']= search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model= Task
    context_object_name= 'task'
    template_name= 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task 
    #dont want to show all the users only title desciption etc
    fields = ['title', 'description', 'complete']
    success_url= reverse_lazy('tasks')

    #only that particular user can update the tasks 
    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task 
    fields = '__all__'
    success_url= reverse_lazy('tasks')

class DeleteView(DeleteView):
    model = Task 
    context_object_name= 'task'
    success_url= reverse_lazy('tasks')

class CustomLoginView(LoginView):
    template_name= 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name= 'base/register.html'
    #this is the built in user creation form and passed it as form in the register.html
    form_class= UserCreationForm
    redirect_authenticated_user= True 
    success_url= reverse_lazy('tasks')

    #redirect the user once the form is submitted
    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

