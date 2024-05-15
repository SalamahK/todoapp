from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/", views.category, name="category"),
    path("add_category/", views.add_category, name="add_category"),
]
