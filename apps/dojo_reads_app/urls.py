from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.main),
    path('books/add', views.add_book),
    path('books/<int:id_book>', views.book_info),
    path('delete/<int:id_review>', views.delete_review),
    path('users/<int:id_user>', views.user_info),
]