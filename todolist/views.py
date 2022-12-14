import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.shortcuts import render
from todolist.models import Task
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from todolist.forms import TaskForm

@login_required(login_url='/todolist/login/')

def show_task(request):
    data_todolist = Task.objects.filter(user=request.user)
    context = {
        'list_task': data_todolist,
        'last_login': request.COOKIES['last_login']
    }
    return render(request, "todolist.html", context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            response = HttpResponseRedirect(reverse("todolist:show_task")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    return response

def create_task(request):
    form = TaskForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            Task.objects.create(title=title, description=description, date=datetime.datetime.now(), user=request.user)
            return redirect('todolist:show_task')
        else :
            form = TaskForm()
    return render(request, 'createtask.html', {'form':form})

def finished_task(request,id):
    task = Task.objects.get(id = id)
    task.is_finished = not(task.is_finished)
    task.save()
    return redirect('todolist:show_task')

def delete_task(request,id):
    task = Task.objects.get(id = id)
    task.delete()
    return redirect('todolist:show_task')

def get_todolist_json (request):
    tasks = Task.objects.filter(user=request.user)
    task_serializers = serializers.serialize('json', tasks)
    return HttpResponse(task_serializers)

def add_todolist_ajax (request):
    if request.method == 'POST':
        title = request.POST.get("title")
        description = request.POST.get("description")

        new_task = Task(user=request.user, title=title, description=description, date=datetime.datetime.now())
        new_task.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

