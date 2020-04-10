from django import forms
from timesheetViewer.models import TestDates

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = TestDates
        fields = [
            'date',
            'start_at',
            'end_at',
            'span'
        ]
