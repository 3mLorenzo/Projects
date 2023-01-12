from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.http import JsonResponse
import json

from .models import Category, Task, User, CategoryForm, TaskForm
# Create your views here.

def index(request):
    return render(request, 'clock/base.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'clock/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    return render(request, 'clock/task_detail.html', {'task': task})

@login_required
def task_create(request):
    tasks = Task.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return render(request, 'clock/task_list.html', {'tasks': tasks})
    else:
        form = TaskForm()
    return render(request, 'clock/task_create.html', {'form': form})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    tasks = Task.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return render(request, 'clock/task_list.html', {'tasks': tasks})
    else:
        form = TaskForm(instance=task)
    return render(request, 'clock/task_update.html', {'form': form})

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)
        task.completed = data['completed']
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    tasks = Task.objects.filter(user=request.user)
    if request.method == 'POST':
        task.delete()
        return render(request, 'clock/task_list.html', {'tasks': tasks})
    context = {
        'task': task
    }
    return render(request, 'clock/task_delete.html', context)

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'clock/category_list.html', {'categories': categories})

@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id, user=request.user)
    return render(request, 'clock/category_detail.html', {'category': category})

@login_required
def category_create(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return render(request, 'clock/category_list.html', {'categories': categories})
    else:
        form = CategoryForm()
    return render(request, 'clock/category_create.html', {'form': form})

@login_required
def category_update(request, category_id):
    category = get_object_or_404(Category, pk=category_id, user=request.user)
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return render(request, 'clock/category_list.html', {'categories': categories})
    else:
        form = CategoryForm(instance=category)
    return render(request, 'clock/category_update.html', {'form': form})

@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        category.delete()
        return render(request, 'clock/category_list.html', {'categories': categories})
    context = {
        'category': category
    }
    return render(request, 'clock/category_delete.html', context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "clock/base.html")
        else:
            return render(request, "clock/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "clock/login.html")


def logout_view(request):
    logout(request)
    return render(request, "clock/base.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "clock/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "clock/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, "clock/base.html")
    else:
        return render(request, "clock/register.html")
