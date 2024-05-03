from . import views
from django.urls import path

urlpatterns = [
  path("", views.index, name="index"),
  path("category", views.category, name="category"),
  path('add_category/', views.add_category, name='add_category')
]