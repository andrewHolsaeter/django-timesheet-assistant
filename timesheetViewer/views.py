from django.shortcuts import render
from django.http import HttpResponse

from timesheetViewer.models import Projects, SubProjects, TestDates

# Create your views here.
def index(request):
    return render(request, "base.html")

def project_list(request):
    proj_sub_proj_obj = Projects.objects.raw("""
        SELECT p.id, p.name, array_agg(sp.description) as descriptions, array_agg(sp.id) as subprojects 
        FROM projects p
        LEFT JOIN sub_projects sp ON p.id = sp.project_id
        GROUP BY p.id
        ORDER BY p.name;
        """)

    context = {
        "projects": proj_sub_proj_obj
    }
    return render(request, "projects.html",  context)