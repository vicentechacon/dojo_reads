from django.contrib import messages
from django.shortcuts import render, redirect
from .models import * 
from apps.login_project_app.models import Usuario
from django.core.exceptions import PermissionDenied

def index(request):
    return redirect('/auth')

def main(request):
    if 'id' not in request.session:
        return redirect('/auth')
    if request.method == 'GET':
        user = Usuario.objects.get(id=request.session['id'])
        books = Book.objects.all()
        reviews = Review.objects.all().order_by('-id')[:3]
        context ={
            'books' : books,
            'user' : user,
            'recent_reviews':reviews
        }
        return render(request, 'main.html', context)
        
def add_book(request):
    if 'id' not in request.session:
        return redirect('/auth')

    if request.method=='GET':
        return render(request,'add_book.html')
    elif request.method == 'POST':
        review_errors=Review.objects.review_validator(request.POST)
        print(review_errors)
        errors=Book.objects.book_validator(request.POST)
        errors.update(review_errors)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/books/add')

        user = Usuario.objects.get(id=request.session['id'])
        new_book = Book.objects.create(
            title = request.POST['title'],
            author = request.POST['author'],
        )
        print(new_book)
        new_book.save()
        new_review = Review.objects.create(
            content = request.POST['content'],
            rating = request.POST['rating'],
            book= new_book,
            reviewer=user
        )
        new_review.save()
        print(new_review)
        return redirect(f'/books/{new_book.id}')

def book_info(request, id_book):
    book = Book.objects.get(id=id_book)
    if 'id' in request.session:

        if request.method=='GET':
            reviews = Review.objects.filter(book_id=id_book)
            context = {
                'book' : book,
                'reviews': reviews
            }
            return render(request, 'book_info.html', context)

        elif request.method =='POST':
            review_errors=Review.objects.review_validator(request.POST)
            errors = Book.objects.book_validator(request.POST)
            errors.update(review_errors)
            if len(errors)>0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/books/{id_book}')

            reviewer = Usuario.objects.get(id=request.session['id'])
            new_review = Review.objects.create(
                content = request.POST['content'],
                rating = request.POST['rating'],
                book = book,
                reviewer = reviewer
            )
            new_review.save()
        return redirect(f'/books/{book.id}')

def delete_review(request, id_review):
    review = Review.objects.get(id=id_review)
    if review.reviewer.id != request.session['id']:
        raise PermissionDenied
    review.delete()
    return redirect('/books')

def user_info(request, id_user):
    user = Usuario.objects.get(id=id_user)
    reviews = user.books_reviewed.all()
    context = {
        'user':user,
        'reviews':reviews
    }
    return render(request,'user_info.html', context)




    


