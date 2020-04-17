from django import forms
from django.utils.translation import gettext_lazy as _
from timesheetViewer.models import Entries, Projects, SubProjects

class MultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())

class SelectForm(forms.Form):
    project = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id':'old-select-item-project',
                'onchange':'fillSubProjects()'}))

    sub_project = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id':'old-select-item-sub-project',
                'onchange':'displayFullId()'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        proj = Projects.objects.all()
        self.fields['project'].choices = (
            (project.id, project.name) for project in proj)
        self.fields['sub_project'].choices = (
            (sp.index, sp.description) for sp in SubProjects.objects.filter(project=proj[0].id))

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
                'onchange':'displayFullId()'}))
    start_at = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required=False)
    end_at   = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required=False)
    #sub_project_id = forms.CharField(max_length=2, required=True, disabled=True)
    span = forms.DurationField(required=False)
    #full_project_id = forms.CharField(max_length=9, label="Project", disabled=True, required=False)
    
    class Meta:
        model = Entries
        fields = [
            'project',
            'sub_project',
            'sub_project_index',
            'day',
            'start_at',
            'end_at',
            'span'
        ]
        labels = {
            'sub_project_index' : _('Sub Project'),
            'start_at' : _('Start'),
            'end_at' : _('End'),
        }
    def __init__(self, *args, **kwargs):
        super(TimesheetForm, self).__init__(*args,**kwargs)
        self.fields['sub_project_index'].widget = forms.HiddenInput()

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

