from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Todo

def login_view(request):
    if request.method == 'POST':
        print('post 데이터', request.POST)
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        print('authenticate 결과', user)
        if user:
            login(request, user)
            return redirect('todo_list')
        return render(request, 'todos/login.html', {'error': '로그인 실패'})
    return render(request, 'todos/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todos/todo_list.html', {'todos': todos})

@login_required
def add_todo(request):
    if request.method == 'POST':
        Todo.objects.create(
            user=request.user,
            title=request.POST['title'],
        )
        return redirect('todo_list')

