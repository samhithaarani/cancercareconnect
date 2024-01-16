from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class CustomAdminDateWidget(DatePickerInput):
    template_name = 'widgets/custom_datepicker.html'

class CustomAdminDateTimeWidget(forms.widgets.DateTimeInput):
    template_name = 'widgets/custom_datetimepicker.html'

