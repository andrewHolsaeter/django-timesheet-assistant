from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Projects, SubProjects, TestDates
from .multiforms import MultiFormsView
from .forms import TimesheetForm, SelectForm

from datetime import datetime

def load_sub_projects(request):
    proj_id = request.GET.get('project_id')
    sub_projects = SubProjects.objects.filter(project_id=proj_id)
    return render(request, 'sub_projects.html', {'sub_projects':sub_projects})

def load_timesheet(request):
    entries = TestDates.objects.all()
    return render(request, 'timesheet_entries.html', {'timesheet_entries':entries})

def form_redir(request):
    return render(request, 'pages/form_redirect.html')

def multiple_forms(request):
    if request.method == 'POST':
        select_form = SelectForm(request.POST)
        timesheet_form = TimesheetForm(request.POST)

        if select_form.is_valid() or timesheet_form.is_valid():
            # Do stuff I need
            return HttpResponseRedirect(reverse('form-redirect'))
    else:
        select_form = SelectForm()
        timesheet_form = TimesheetForm(initial={'date': datetime.today(),'start_at':datetime.now()})

    context = {
        'select_form': select_form,
        'timesheet_form': timesheet_form,
    }

    return render(request, 'clock.html', context)


class MultpleFormsTestView(MultiFormsView):
    template_name = 'clock.html'
    form_classes = {
        'select_form':SelectForm,
        'timesheet_form':TimesheetForm,
    }

    success_urls = {
        'select_form':reverse_lazy('form-redirect'),
        'timesheet_form':reverse_lazy('timesheet_form'),
    }

    def select_form_valid(self, form):
        select = form.cleaned_data.get('select')
        form_name = form.cleaned_data.get('action')
        print(select)
        return HttpResponseRedirect(self.get_success_url(form_name))

    def timesheet_form_valid(self, form):
        form_name = form.cleaned_data.get('action')
        return HttpResponseRedirect(self.get_success_url(form_name))

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
