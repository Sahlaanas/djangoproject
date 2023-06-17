from django import forms
from .models import User_Address
import re

class AddressForm(forms.ModelForm):
    class Meta:
        model = User_Address
        fields = ['firstname','lastname','contact_number','address','city',  'pincode', 'district', 'state','country']
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs )
        
        self.fields['firstname'].widget.attrs['placeholder'] = 'First Name'
        self.fields['firstname'].widget.attrs['data-type'] = 'form-text'

        self.fields['lastname'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['lastname'].widget.attrs['data-type'] = 'form-text'
        
        self.fields['contact_number'].widget.attrs['placeholder'] = 'Mobile'
        self.fields['contact_number'].widget.attrs['data-type'] = 'form-number'

      

        self.fields['address'].widget.attrs['placeholder'] = 'Address'
        self.fields['address'].widget.attrs['data-type'] = 'form-text'

        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['city'].widget.attrs['data-type'] = 'form-text'

        self.fields['pincode'].widget.attrs['placeholder'] = 'Pincode'
        self.fields['pincode'].widget.attrs['data-type'] = 'form-number'

        self.fields['district'].widget.attrs['placeholder'] = 'District'
        self.fields['district'].widget.attrs['data-type'] = 'form-text'

        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['state'].widget.attrs['data-type'] = 'form-text'

        self.fields['country'].widget.attrs['placeholder'] = 'Country'
        self.fields['country'].widget.attrs['data-type'] = 'form-text'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-md w-100'


    def clean_firstname(self):
        firstname = self.cleaned_data['firstname']
        if not re.match(r'^[a-zA-Z ]+$', firstname):
            raise forms.ValidationError("Name can only contain alphabets and spaces.")
        return firstname
    
    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        if str(contact_number).startswith('0'):
            raise forms.ValidationError('Phone number should not start with zero')
        if len(str(contact_number)) < 10:
            raise forms.ValidationError('Phone number should have minimum 10 numbers without start with zero')
        if len(str(contact_number)) > 12:
            raise forms.ValidationError('Phone number never greater than 12')
        return contact_number