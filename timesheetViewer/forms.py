from django import forms
from timesheetViewer.models import TestDates, Projects, SubProjects

class MultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = TestDates
        fields = [
            'date',
            'start_at',

            'end_at',
            'span'
        ]
    
class ProjectDropDownForm(MultipleForm):
    project = forms.ChoiceField(widget=forms.Select(attrs={'id':'select-project',
    'onchange':'fillSubProjects()'}))
    # projects = forms.ModelChoiceField(queryset=Projects.objects.all(), empty_label="Selected value")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].choices = [(project.id, project.name) for project in Projects.objects.all()]
    #     self.fields

class SubProjectDropDownForm(MultipleForm):
    sub_project = forms.ChoiceField(widget=forms.Select(attrs={'id':'select-sub-project'}))
    # projects = forms.ModelChoiceField(queryset=Projects.objects.all(), empty_label="Selected value")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_project'].choices = [(project.id, project.description) for project in SubProjects.objects.all()]
    #     self.fields

class SelectForm(forms.Form):
    project = forms.ChoiceField(widget=forms.Select(attrs={'id':'select-item-project',
    'onchange':'fillSubProjects()'}))
    sub_project = forms.ChoiceField(widget=forms.Select(attrs={'id':'select-item-sub-project'}))

    # projects = forms.ModelChoiceField(queryset=Projects.objects.all(), empty_label="Selected value")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        proj = Projects.objects.all()
        self.fields['project'].choices = [(project.id, project.name) for project in proj]
        self.fields['sub_project'].choices = [(sp.id, sp.description) for sp in SubProjects.objects.filter(project=proj[0].id)]

    
    def update_sub_projects(self, selected_proj):
        self.fields['sub_project'].choices = [(sp.id, sp.description) for sp in SubProjects.objects.filter(project=selected_proj)]
    #     self.fields

class SelectSubProjectForm(forms.ModelForm):
    sub_project = forms.ChoiceField(widget=forms.Select(attrs={'id':'select-sub-project'}))
    
    class Meta:
        model = SubProjects
        fields = ('id','description')

    # projects = forms.ModelChoiceField(queryset=Projects.objects.all(), empty_label="Selected value")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_project'].choices = [(project.id, project.description) for project in SubProjects.objects.all()]
    #     self.fields