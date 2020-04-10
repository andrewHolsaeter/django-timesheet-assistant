from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from timesheetViewer.models import Projects, SubProjects, TestDates
from timesheetViewer.forms import TimesheetForm

from datetime import datetime

# Create your views here.
def index(request):
    return render(request, "base.html")

def clock(request):
    # Change to selected
    projects = Projects.objects.all()
    sub_projects = SubProjects.objects.all()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TimesheetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # book_instance.due_back = form.cleaned_data
            # book_instance.save()
            data = form.cleaned_data
            # redirect to a new URL:
            


    # if a GET (or any other method) we'll create a blank form
    else:
        form = TimesheetForm(initial={'date': datetime.today(),'start_at':datetime.now()})
    

    dates = TestDates.objects.all()
    context = {
        "projects":projects,
        "subprojects":sub_projects,
        "form":form,
        "dates": dates
    }
    
    return render(request, "clock.html", context)

def project_list(request):
    proj_sub_proj_obj = Projects.objects.raw("""
        SELECT p.id, p.name, array_agg(sp.description) as descriptions, array_agg(sp.id) as subprojects 
        FROM projects p
        LEFT JOIN sub_projects sp ON p.id = sp.project_id
        GROUP BY p.id
        ORDER BY p.name;
        """)

    project_sub_project = {}
    for r in proj_sub_proj_obj:
        proj = r.name
        project_sub_project[proj] = {}
        j = 0
        for d in r.descriptions:
            # Get index
            project_sub_project[proj][d] = r.id + '-' + r.subprojects[j]
            j += 1

    context = {
        "projects": proj_sub_proj_obj,
        "sub_project_ful_ids": project_sub_project
    }
    return render(request, "projects.html", context)
