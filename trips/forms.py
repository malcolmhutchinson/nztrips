from django import forms
from models import Trip


class TripRecord(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'name',
            'trip_type',
            'subject',
            'description',
            'location',
            'days_length',
        ]

        labels = {
            'days_length': 'Duration (days)',


        }

class UploadFile(forms.Form):
    uploadFile = forms.FileField(required=False)

        
