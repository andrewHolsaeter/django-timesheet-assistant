from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.db import connection

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

def generate_timesheet(request):
    cursor = connection.cursor()

    week = request.GET.get('week')
    year = request.GET.get('year')
    
    # Get weekdays
    cursor.execute(f"""
        SELECT DATE(day)
        FROM generate_series(
            date_trunc('day', to_date('{year}{week}', 'iyyyiw')),
            date_trunc('day', to_date('{year}{week}', 'iyyyiw') + 6),
            '1 day') day
    """)
    # Get weekdays
    weekdays = [x[0] for x in cursor.fetchall()]
    weekday_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']


    # Get distinct sub_projects
    cursor.execute(f"""
    SELECT distinct sub_project_id
    FROM test_dates
    WHERE to_char(date, 'IW') = '{week}'
    AND to_char(date, 'YYYY') = '{year}';
    """)
    sub_projects = cursor.fetchall()

    # Get relevant week's timesheet entries
    cursor.execute(f"""
    SELECT 
        d.date,
        sp.project_id,
        sp.index,
        date_trunc('minute',
            SUM( CASE
                WHEN d.span IS NOT NULL THEN d.span
                WHEN d.start_at IS NOT NULL AND d.end_at IS NOT NULL THEN d.end_at - d.start_at
                ELSE NULL
                END)) AS hours
    FROM test_dates d
    JOIN sub_projects sp ON d.sub_project_id = sp.index
    WHERE to_char(d.date, 'IW') = '{week}'
    AND to_char(date, 'YYYY') = '{year}'
    GROUP BY d.date, sp.project_id, sp.index
    ORDER BY d.date, sp.project_id, sp.index;
    """)
    hours = cursor.fetchall()

    hours_dict = {}
    # Fill timesheet sub projects with blank/0 hours
    for sp in sub_projects:
        hours_dict[sp[0]] = []
        
        for wd in weekdays:
            hours_dict[sp[0]].append(0)

    # Fill in the blanked timesheet with the actual values
    # from the rows returned from the main query
    for entry in hours:
        date = entry[0]
        sp = entry[2]

        # Get day of the week index the date corresponds to
        # i.e. 2020-04-07 is a Wednesday, so indx would be 3
        indx = weekdays.index(date)
        hours_dict[sp][indx] = entry[3]

    context = {
        'weekdays':weekday_names,
        'hours':hours_dict
    }

    return render(request, 'generated_timesheet.html', context)

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
