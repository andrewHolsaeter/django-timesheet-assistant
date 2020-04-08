from django.shortcuts import render
from django.http import HttpResponse

from timesheetViewer.models import Projects, SubProjects, TestDates

# Create your views here.
def index(request):
    return render(request, "base.html")

def project_list(request):
    projects_obj = Projects.objects.all()
    
    context = {
        "projects": projects_obj
    }
    return render(request, "projects.html",  context)