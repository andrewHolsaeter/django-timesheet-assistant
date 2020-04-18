from django.shortcuts import render
from django.urls import path

# Create your views here.
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.project_list, name='projects'),
    path('clock/', views.clock, name='clock'),
    path('ajax/load_sub_projects/', views.load_sub_projects, name='ajax_load_sub_projects'),
    path('ajax/load_timesheet/', views.load_timesheet, name='ajax_load_timesheet'),
    path('ajax/generate_timesheet/', views.generate_timesheet, name='ajax_generate_timesheet'),
    path('ajax/insert_time_entry/', views.insert_time_entry, name='ajax_insert_time_entry'),
    path('ajax/delete_entries/', views.delete_entries, name='ajax_delete_entries'),
    path('ajax/show_toast/', views.show_toast, name='ajax_show_toast')
]
