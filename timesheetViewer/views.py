from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Projects, SubProjects, TestDates
from .forms import TimesheetForm, ProjectDropDownForm, SubProjectDropDownForm, SelectForm, SelectSubProjectForm
from .multiforms import MultiFormsView

from datetime import datetime

def load_sub_projects(request):
    proj_id = request.GET.get('project_id')
    sub_projects = SubProjects.objects.filter(project_id=proj_id)
    return render(request, 'sub_projects.html', {'sub_projects':sub_projects})

def form_redir(request):
    return render(request, 'pages/form_redirect.html')

def multiple_forms(request):
    if request.method == 'POST':
        project_form = ProjectDropDownForm(request.POST)
        sub_project_form = SubProjectDropDownForm(request.POST)
        select_form = SelectForm(request.POST)

        if project_form.is_valid() or sub_project_form.is_valid():
            # Do stuff I need
            return HttpResponseRedirect(reverse('form-redirect'))
    else:
        project_form = ProjectDropDownForm()
        sub_project_form = SubProjectDropDownForm()
        select_form = SelectForm()

    context = {
        'project_form': project_form,
        'sub_project_form': sub_project_form,
        'select_form': select_form,
    }

    return render(request, 'clock.html', context)


class MultpleFormsTestView(MultiFormsView):
    template_name = 'clock.html'
    form_classes = {
        'project':ProjectDropDownForm,
        'sub_project':SubProjectDropDownForm,
        'select_form':SelectForm,
    }

    success_urls = {
        'project':reverse_lazy('form-redirect'),
        'sub_project':reverse_lazy('form-redirect'),
        'select_form':reverse_lazy('form-redirect'),
    }

    def project_form_valid(self, form):
        select = form.cleaned_data.get('select')
        form_name = form.cleaned_data.get('action')
        print(select)
        return HttpResponseRedirect(self.get_success_url(form_name))

    def sub_project_form_valid(self, form):
        select = form.cleaned_data.get('select')
        form_name = form.cleaned_data.get('action')
        print(select)
        return HttpResponseRedirect(self.get_success_url(form_name))

    def select_form_valid(self, form):
        select = form.cleaned_data.get('select')
        form_name = form.cleaned_data.get('action')
        print(select)
        return HttpResponseRedirect(self.get_success_url(form_name))

# Create your views here.
def index(request):
    return render(request, "base.html")


def clock(request):
    # Change to selected
    projects = Projects.objects.all()
    sub_projects = SubProjects.objects.all()
    # project_form = ProjectDropDownForm()
    select_form = SelectForm()
    sub_project_form = SelectSubProjectForm()

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
        # "project-form": project_form,
        "sub-project-form": sub_project_form,
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
