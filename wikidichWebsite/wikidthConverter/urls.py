from django.urls import path
from . import views

app_name = "wikidithConverter"

urlpatterns = [
    path('', views.index, name="index"),
    path('booklist/', views.all_books, name="booklist")
]