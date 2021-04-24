from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager, Book, BookManager
import bcrypt

def index(request):
    return render(request, 'register_login.html')

def books(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        context = {
            'user': user[0],
            'all_books': Book.objects.all()
        }
        return render(request, 'books.html', context)
    else:
        return redirect('/')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        user = User.objects.create(
            first_name = request.POST['first_name'], 
            last_name = request.POST['last_name'], 
            email = request.POST['email'],
            password = hash_pw
            )
        request.session['user_id'] = user.id
        return redirect('/books')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = user[0].id
        return redirect('/books')
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def add_book(request):
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        
        user = User.objects.filter(id=request.session['user_id'])
        book = Book.objects.create(
            title=request.POST['title'], 
            desc=request.POST['desc'], 
            uploaded_by=user[0]
            )
        user[0].liked_books.add(book)
        return redirect('/books')
    else:
        return redirect('/books')

def book_content(request, book_id):
    user = User.objects.filter(id=request.session['user_id'])
    context = {
        'book': Book.objects.get(id=book_id),
        'user': user[0]
    }
    return render(request, 'book_content.html', context)

def update(request, book_id):
    book = Book.objects.get(id=book_id)
    book.desc = request.POST['desc']
    book.save()
    return redirect(f'/books/{book_id}')

def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')

def add_favorite(request, book_id):
    user = User.objects.filter(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user[0].liked_books.add(book)
    return redirect(f'/books/{book_id}')

def remove_favorite(request, book_id):
    user = User.objects.filter(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user[0].liked_books.remove(book)
    return redirect(f'/books/{book_id}')
