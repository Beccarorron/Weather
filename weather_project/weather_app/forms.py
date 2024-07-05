from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from crispy_forms.helper import FormHelper
from django.forms import TextInput
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Submit, Field
from crispy_bootstrap5.bootstrap5 import FloatingField

statechoices = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming')
]
class DateTimeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        include_end_date = kwargs.pop('include_end_date', True)  # Default to including end_date
        super(DateTimeForm, self).__init__(*args, **kwargs)
        self.fields['begin_date'] = forms.DateTimeField(
            widget=DateTimePickerInput(options={"format": "YYYY/MM/DD HH:00:00"})
        )
        if include_end_date:
            self.fields['end_date'] = forms.DateTimeField(
                widget=DateTimePickerInput(options={"format": "YYYY/MM/DD HH:00:00"})
            )
class NewForm(forms.Form):
    city = forms.CharField(label="City", widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control form-label'}))
    state = forms.ChoiceField(label="State", choices=statechoices, widget=forms.Select(attrs={'class': 'form-select, form-control, form-label'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))
        
class CombinedForm(forms.Form):
    def __init__(self, *args, **kwargs):
        include_end_date = kwargs.pop('include_end_date', True)  # Default to including end_date
        super(CombinedForm, self).__init__(*args, **kwargs)
        self.fields['city'] = forms.CharField(label="City", widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control form-label'}))
        self.fields['state'] = forms.ChoiceField(label="State", choices=statechoices, widget=forms.Select(attrs={'class': 'form-select, form-control, form-label'}))
        self.fields['begin_date'] = forms.DateTimeField(
            widget=DateTimePickerInput(options={"format": "YYYY/MM/DD HH:00:00"})
        )
        if include_end_date:
            self.fields['end_date'] = forms.DateTimeField(
                widget=DateTimePickerInput(options={"format": "YYYY/MM/DD HH:00:00"})
            )       
    
    
        
        
