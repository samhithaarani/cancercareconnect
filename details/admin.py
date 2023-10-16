from django.contrib import admin
from django import forms
from django.db import models
from .models import Patient, PatientAdditionalInfo, AdminManagedUser, PatientImage, Control

class PatientAdditionalInfoInline(admin.StackedInline):
    model = PatientAdditionalInfo

class PatientImageForm(forms.ModelForm):
    class Meta:
        model = PatientImage
        fields = ("patient", "image")


class PatientImageInline(admin.TabularInline):
    model = PatientImage
    form = PatientImageForm

class ControlInline(admin.TabularInline):
    model = Control
    extra = 1  # You can adjust the number of inline forms displayed for controls

class PatientAdmin(admin.ModelAdmin):
    inlines = [PatientAdditionalInfoInline, PatientImageInline, ControlInline]
    filter_horizontal = ('ct_images_before', 'ct_images_after')
    list_display = ('first_name', 'last_name', 'primary_tumor', 'num_metastasis', 'mark_for_study') 

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ForeignKey: {'limit_choices_to': {'field_name__icontains': 'specific_value'}}
    }

class AdminManagedUserAdmin(admin.ModelAdmin):
    list_display = ('username',)

class PatientImageAdmin(admin.ModelAdmin):
    form = PatientImageForm

class ControlAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'details')

admin.site.register(AdminManagedUser, AdminManagedUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientImage, PatientImageAdmin)
admin.site.register(Control, ControlAdmin)  # Register the ControlAdmin class
