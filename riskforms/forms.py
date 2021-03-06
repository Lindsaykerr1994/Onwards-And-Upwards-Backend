from django import forms
from .models import Participant, RAForm


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        exclude = ('appointment', 'client')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date Of Birth',
            'email_address': 'Email Address',
            'phone_number': 'Phone Number',
            'address_line1': 'Street Address 1',
            'address_line2': 'Street Address 2',
            'address_line3': 'Street Address 3',
            'town_or_city': 'Town Or City',
            'postcode': 'Post Code',
            'emergency_contact_name': 'Name',
            'emergency_contact_number': 'Tel',
        }
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'onwards-form-input'
            self.fields[field].label = True


class RiskAcknowledgementForm(forms.ModelForm):

    class Meta:
        model = RAForm
        exclude = ('form_number', 'date_created')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
