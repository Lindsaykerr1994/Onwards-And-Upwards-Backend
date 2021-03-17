from django import forms
from .models import Participant


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        exclude = ('appointment', 'client', 'manual_form')

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
            'dec_illness': 'Declaration Of Illness',
            'dec_medication': 'Declaration Of Medication',
            'dec_abs_cond': 'Declaration Of Absence of Condition',
            'acknowledgement_of_risk': 'Acknowledgement',
            'signed_by': 'Signed By',
            'date_signed': 'Date Signed'
        }
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'onwards-form-input'
            self.fields[field].label = True
