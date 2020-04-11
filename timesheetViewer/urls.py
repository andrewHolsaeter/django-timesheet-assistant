from django.shortcuts import render
from django.urls import path

# Create your views here.
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.project_list, name='projects'),
    path('clock/', views.multiple_forms, name='clock'),
    path('ajax/load_sub_projects/', views.load_sub_projects, name='ajax_load_sub_projects'),
    path('ajax/load_timesheet/', views.load_timesheet, name='ajax_load_timesheet')
]