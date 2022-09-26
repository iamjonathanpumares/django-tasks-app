from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Task
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TaskForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('tasks')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    active_tab = 'all'
    return render(request, 'tasks.html', {'tasks': tasks, 'active_tab': active_tab})

@login_required
def tasks_pending(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    active_tab = 'pending'
    return render(request, 'tasks.html', {'tasks': tasks, 'active_tab': active_tab})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False)
    active_tab = 'completed'
    return render(request, 'tasks.html', {'tasks': tasks, 'active_tab': active_tab})

@login_required
def task_new(request):
    action = 'Create'
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'action': action})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    action = 'Edit'
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'task': task, 'action': action})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.date_completed = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})
