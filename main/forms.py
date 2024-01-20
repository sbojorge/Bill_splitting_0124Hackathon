from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    eventName = forms.CharField(label='Event Name', max_length=200)
    member1 = forms.CharField(label='Member 1', max_length=100, required=False)
    member2 = forms.CharField(label='Member 2', max_length=100, required=False)
    member3 = forms.CharField(label='Member 3', max_length=100, required=False)
    member4 = forms.CharField(label='Member 4', max_length=100, required=False)
    member5 = forms.CharField(label='Member 5', max_length=100, required=False)
    member6 = forms.CharField(label='Member 6', max_length=100, required=False)
    member7 = forms.CharField(label='Member 7', max_length=100, required=False)
    member8 = forms.CharField(label='Member 8', max_length=100, required=False)
    member9 = forms.CharField(label='Member 9', max_length=100, required=False)
    member10 = forms.CharField(label='Member 10', max_length=100, required=False)

    class Meta:
        model = Event
        fields = [
            'eventName', 'member1', 'member2', 'member3',
            'member4', 'member5', 'member6', 'member7', 'member8',
            'member9', 'member10'
            ]
