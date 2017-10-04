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
        ]

class UploadFile(forms.Form):
    uploadFile = forms.FileField(required=False)

        
