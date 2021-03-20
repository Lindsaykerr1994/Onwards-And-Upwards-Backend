from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        exclude = ('created_date', 'appointment_number', 'client', 'isPaid')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'activity': 'Select An Activity',
            'course': 'Select A Course',
            'appointment_date': 'Date',
            'appointment_time': 'Time',
            'appointment_participants': 'Number Of Participants',
            'appointment_location': 'Location',
            'isSolo': 'Solo/Group',
            'appointment_price': 'Price',
            'add_notes': 'Additional Notes'
        }
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'onwards-form-input'
            self.fields[field].label = True
