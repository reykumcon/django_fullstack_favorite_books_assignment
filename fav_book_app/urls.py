from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.books),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books/add_book', views.add_book),
    path('books/<int:book_id>', views.book_content),
    path('books/<int:book_id>/update', views.update),
    path('books/<int:book_id>/delete', views.delete),
    path('books/<int:book_id>/add_favorite', views.add_favorite),
    path('books/<int:book_id>/remove_favorite', views.remove_favorite),
]