from django.shortcuts import render
from django.urls import path

# Create your views here.
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path("<int:pk>/", views.project_list, name="project_list"),
    path('projects/', views.project_list, name='projects'),
    path('clock/', views.clock, name='clock'),
]