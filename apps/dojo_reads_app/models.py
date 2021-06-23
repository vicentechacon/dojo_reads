import re
from django.db import models
from apps.login_project_app.models import Usuario

# Create your models here.

class BookManager(models.Manager):
    def book_validator(self, postData):
        book_errors = {}
        if 'title' in postData and len(postData['title']) < 2:
            book_errors['title']='Title should be at least 2 characters'
        if 'author' in postData and len(postData['author']) < 1:
            book_errors['author'] ='Author is required'
            
        return book_errors

class ReviewManager(models.Manager):
    def review_validator(self, postData):
        review_errors ={}
        print(postData['rating'])
        if int(postData['rating'])<0 or int(postData['rating'])>5 :
            review_errors['rating']='Rating is required'
        if len(postData['content'])<5:
            review_errors['content']='Content should be at least 5 characters'

        return review_errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='books_reviewed')
    objects=ReviewManager()

