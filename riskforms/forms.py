from django import forms
from .models import Participant


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        exclude = ('form_number', 'appointment', 'date_created',
                   'client', 'risk_form')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date Of Birth',
            'email_address': 'Email Address',
            'phone_number': 'Phone Number',
            'address_line': 'Address',
            'postcode': 'Post Code',
            'emergency_contact_name': 'Name',
            'emergency_contact_number': 'Tel',
            'dec_illness': 'Illness',
            'dec_medication': 'Mediciation',
            'dec_abs_cond': 'Absence of An Existing Condition',
            'acknowledgement_of_risk': 'Acknowledgement of Risk',
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
