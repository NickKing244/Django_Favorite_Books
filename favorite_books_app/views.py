from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == 'POST':
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['userid'] = User.objects.last().id
            print(request.session['userid'])
            return redirect('/books')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            request.session['userid'] = user.id
            print(request.session['userid'])
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                return redirect('/books')
        messages.error(request, "Email or password are not correct")
    return redirect('/')

def main(request):
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user': user,
        'all_books': Book.objects.all()
    }
    if 'userid' not in request.session:
        return redirect('/')
    else:
        return render(request, 'main_page.html', context)

def add_book(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        this_user = User.objects.get(id=request.session['userid'])
        book = Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], uploaded_by=this_user)
        book.users_who_like.add(this_user)
        return redirect('/books')

def show_book(request, book_id):
    this_book = Book.objects.get(id=book_id)
    context = {
        'book': this_book,
        'this_user': User.objects.get(id=request.session['userid']),
    }
    return render(request, 'update.html', context)

def update(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')
    this_book = Book.objects.get(id=book_id)
    this_book.desc = request.POST['desc']
    this_book.save()
    return redirect(f'/books/{book_id}')

def favorite(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')
    this_book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['userid'])
    user.liked_books.add(this_book)
    return redirect(f'/books/{book_id}')

def unfavorite(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')
    this_book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['userid'])
    user.liked_books.remove(this_book)
    return redirect(f'/books/{book_id}')

def delete(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')
    if request.method =='POST':
        logged_user = User.objects.get(id=request.session['userid'])
        if logged_user.id == Book.uploaded_by.id:
            book = Book.objects.get(id=book_id)
            book.delete()
        else:
            return redirect('/')
    return redirect('/books')

def logout(request):
    request.session.flush()
    return redirect('/')