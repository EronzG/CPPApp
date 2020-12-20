from django import forms
from django.forms.widgets import DateInput


from .models import HealthData, DailyLog, ActivityLog, Photo


class DateInput(DateInput):
    """Changing the date input type"""
    input_type = 'date'


class HealthDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HealthDataForm, self).__init__(*args, **kwargs)

        self.fields['dob'].widget = DateInput()

    class Meta:
        model = HealthData
        fields = ['mass', 'height', 'gender', 'dob']


class DailyLogForm(forms.ModelForm):

    class Meta:
        model = DailyLog
        fields = ['steps', 'mood']


class ActivityLogForm(forms.ModelForm):

    class Meta:
        model = ActivityLog
        fields = ['activity', 'duration']


class Photoform(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['image', 'caption']


class PhotoDownloadForm(forms.Form):
    hidden = forms.HiddenInput()
