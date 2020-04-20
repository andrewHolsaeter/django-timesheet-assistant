from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from timesheetViewer.models import Entries, Projects, SubProjects

from datetime import timedelta
import re

def get_first_number(string):
    # Find first number (will be the second group)
    regex = r'^(\D*)(\d+)'
    match = re.search(regex, string)
    if match:
        number = match.groups()[1]
        return int(number)
    return 0


class CustomDurationField(forms.DurationField):
    def clean(self, value):
        try:
            # if contains years, days, months raise
            tmp = value

            regex = r'([0-9]+.+hour[^0-9]+)'
            match = re.search(regex, tmp)
            if match:
                idx = match.span()[1]
                just_hours = tmp[:idx]
                # rest
                tmp = tmp[idx:]
                hours = get_first_number(just_hours)

            
            regex = r'([0-9]+.+minute[^0-9]+)'
            match = re.search(regex, tmp)
            if match:
                # if match
                idx = match.span()[1]
                just_minutes = tmp[:idx]
                # rest
                tmp = tmp[idx:]
                minutes = get_first_number(just_minutes)
     
            regex = r'([0-9]+.+second[^0-9]+)'
            match = re.search(regex, tmp)
            if match:
                # if match
                idx = match.span()[1]
                just_seconds = tmp[:idx]
                seconds = get_first_number(just_seconds)
            
            if hours or minutes:
                hours = hours or 0
                minutes = minutes or 0
                value = timedelta(hours = hours, minutes=minutes)

            return value
        except:
            raise ValueError

class TimesheetForm(forms.ModelForm):
    project = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id':'select-item-project',
                'onchange':'fillSubProjects()'}))
    sub_project = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id':'select-item-sub-project',
                'onchange':'displayFullId()',
                'data-url': reverse_lazy('ajax_load_sub_projects')}))
    start_at = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required=False)
    end_at   = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required=False)
    #sub_project_id = forms.CharField(max_length=2, required=True, disabled=True)
    span = CustomDurationField(required=False)

    #full_project_id = forms.CharField(max_length=9, label="Project", disabled=True, required=False)
    
    class Meta:
        model = Entries
        fields = [
            'project',
            'sub_project',
            'day',
            'start_at',
            'end_at',
            'span'
        ]
        labels = {
            'start_at' : _('Start'),
            'end_at' : _('End'),
        }
    def __init__(self, *args, **kwargs):
        super(TimesheetForm, self).__init__(*args,**kwargs)

        self.fields['project'].choices = list(Projects.objects.values_list('id', 'name'))
        # If form already has data, use selected project to filter
        if 'project' in self.data:
            try:
                choices = SubProjects.objects.filter(
                    project_id=self.data.get('project')
                    ).order_by('description').values_list('index','description')
                self.fields['sub_project'].choices = choices

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to original queryset
        else:
            proj = Projects.objects.all()
            self.fields['sub_project'].choices = (
                (sp.index, sp.description) for sp in SubProjects.objects.filter(project=proj[0].id))

