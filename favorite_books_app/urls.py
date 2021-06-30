from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/create', views.create_user),
    path('users/login', views.login),
    path('users/logout', views.logout),
    path('books', views.main),
    path('books/create', views.add_book),
    path('books/<int:book_id>', views.show_book),
    path('books/<int:book_id>/update', views.update),
    path('books/<int:book_id>/delete', views.delete),
    path('books/<int:book_id>/favorite', views.favorite),
    path('books/<int:book_id>/unfavorite', views.unfavorite),
]