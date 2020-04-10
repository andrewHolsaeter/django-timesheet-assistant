from django import forms
from django.utils.translation import gettext_lazy as _
from timesheetViewer.models import TestDates, Projects, SubProjects

class MultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())

class SelectForm(forms.Form):
    project = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id':'select-item-project',
                'onchange':'fillSubProjects()'}))

    sub_project = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id':'select-item-sub-project',
                'onchange':'displayFullId()'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        proj = Projects.objects.all()
        self.fields['project'].choices = [
            (project.id, project.name) for project in proj]
        self.fields['sub_project'].choices = [
            (sp.id, sp.description) for sp in SubProjects.objects.filter(project=proj[0].id)]

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = TestDates
        fields = [
            'full_project_id',
            'date',
            'start_at',
            'end_at',
            'span'
        ]
        labels = {
            'full_project_id' : _('Project ID'),
            'start_at' : _('Start'),
            'end_at' : _('End')

        }
