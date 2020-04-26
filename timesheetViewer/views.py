from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.db import connection

from .models import Projects, SubProjects, Entries
from .forms import TimesheetForm

import json
from datetime import datetime

def show_toast(request):
    context = {
        'class' : request.POST.get("class"),
        'msg' : request.POST.get("msg")
    }

    return render(request, 'toast.html', context)

def load_sub_projects(request):
    proj_id = request.GET.get('project_id')
    sub_projects = SubProjects.objects.filter(project_id=proj_id)
    return render(request, 'sub_projects.html', {'sub_projects':sub_projects})

def load_timesheet(request):
    entries = Entries.objects.all()
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
    SELECT distinct sub_project_index
    FROM entries
    WHERE to_char(day, 'IW') = '{week}'
    AND to_char(day, 'YYYY') = '{year}';
    """)
    sub_projects = cursor.fetchall()

    # Get relevant week's timesheet entries
    cursor.execute(f"""
    SELECT 
        d.day,
        sp.project_id,
        sp.index,
        EXTRACT(epoch FROM date_trunc('minute',
            SUM( CASE
                WHEN d.span IS NOT NULL THEN d.span
                WHEN d.start_at IS NOT NULL AND d.end_at IS NOT NULL THEN d.end_at - d.start_at
                ELSE NULL
                END)))/3600 AS hours
    FROM entries d
    JOIN sub_projects sp ON d.sub_project_index= sp.index
    WHERE to_char(d.day, 'IW') = '{week}'
    AND to_char(d.day, 'YYYY') = '{year}'
    GROUP BY d.day, sp.project_id, sp.index
    ORDER BY sp.project_id, sp.index, d.day;
    """)
    hours = cursor.fetchall()

    hours_dict = {}
    # Fill timesheet sub projects with blank/0 hours
    for sp in hours:
        proj = sp[1]+"-"+str(sp[2])
        hours_dict[proj] = []

        for wd in weekdays:
            hours_dict[proj].append(0)

    # Fill in the blanked timesheet with the actual values
    # from the rows returned from the main query
    for entry in hours:
        date = entry[0]
        sp = entry[2]
        proj = entry[1]+"-"+str(entry[2])
        # Get day of the week index the date corresponds to
        # i.e. 2020-04-07 is a Wednesday, so indx would be 3
        indx = weekdays.index(date)
        hours_dict[proj][indx] = entry[3]

    context = {
        'weekdays':weekday_names,
        'hours':hours_dict,
        'title': f"{year}-{week}"
    }

    return render(request, 'generated_timesheet.html', context)

def insert_time_entry(request):
    cursor = connection.cursor()
    data = request.POST.get('post')
    proj = request.POST.get('proj')
    sub_proj = request.POST.get('sub_proj')

    cursor.execute(f"""
    SELECT index
    FROM sub_projects
    LEFT JOIN projects ON (project_id = projects.id)
    WHERE sub_projects.index='{sub_proj}'
    AND project_id='{proj}';
    """)
    indices = cursor.fetchall()
    if len(indices) != 1:
        context = {
            'class':'error',
            'msg':'Sub project index retrieval did not return a single results'
        }
    else:
        index = indices[0][0]
        form = TimesheetForm(request.POST)
        sub_proj_obj = SubProjects.objects.get(pk=index)
        #form.fields["sub_project_index"] = index
        
        if form.is_valid():
            entry = form.save(commit=False)
            entry.sub_project_index = sub_proj_obj
            entry.save()

            context = {
                'class':'success',
                'msg':'Success'
            }
        else:
            context = {
                'class':'error',
                'msg':'Problem inserting entry'
            }

    return render(request, 'toast.html', context)

def delete_entries(request):
    arr = request.POST.get('arr')
    entries = json.loads(arr)
    # Have to use post
    if request.method != 'POST':
        context = {
            'class':'error',
            'msg':'Method was not POST'
        }

    elif len(entries) < 1:
        context = {
            'class':'error',
            'msg':'Entries length was less than 1'
        }

    else:
        # Delete
        Entries.objects.filter(pk__in=entries).delete()
        context = {       
            'class':'succes',
            'msg':'Succesfully deleted:',
            'ul': [li for li in entries]
        }

    return render(request, 'toast.html', context)

def form_redirect(request):
    return render(request, 'toast.html')

def clock(request):
    # Check if I need this POST
    if request.method == 'POST':
        timesheet_form = TimesheetForm(request.POST)

        # if select_form.is_valid() or timesheet_form.is_valid():
        #     # Do stuff I need
        #     return insert_time_entry(request)
        #     #return HttpResponseRedirect(reverse('form-redir'))
    else:
        timesheet_form = TimesheetForm(initial={'day': datetime.today(),'start_at':datetime.now()})

    context = {
        'timesheet_form': timesheet_form,
    }

    return render(request, 'clock.html', context)

# Create your views here.
def index(request):
    return render(request, "base.html")

def timesheet(request):
    context={
        
    }
    return render(request, "timesheet.html")

def project_list(request):
    proj_sub_proj_obj = Projects.objects.raw("""
        SELECT p.id, p.name, array_agg(sp.description) as descriptions, array_agg(sp.activity_number) as subprojects 
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
