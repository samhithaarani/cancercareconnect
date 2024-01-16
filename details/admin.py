from django.contrib import admin
from django import forms
from django.db import models
from .models import Patient, PatientAdditionalInfo, AdminManagedUser, PatientImage, Control, Control_Images
from django.contrib.admin.widgets import AdminDateWidget

class PatientAdditionalInfoInline(admin.StackedInline):
    model = PatientAdditionalInfo

class PatientImageForm(forms.ModelForm):
    class Meta:
        model = PatientImage
        fields = ("patient", "image")

class PatientImageInline(admin.TabularInline):
    model = PatientImage
    form = PatientImageForm

class ControlImagesInline(admin.TabularInline):
    model = Control_Images
    extra = 1

class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'  # Specify all fields or list the fields you want to include
        widgets = {
            'date_of_first_presentation': forms.DateInput(attrs={'type': 'date'}),
        }
class ControlAdminForm(forms.ModelForm):
    class Meta:
        model = Control
        fields = '__all__'  # Specify all fields or list the fields you want to include
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class ControlInline(admin.TabularInline):
    model = Control
    extra = 1

class PatientAdmin(admin.ModelAdmin):
    form = PatientAdminForm
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
    form = ControlAdminForm
    inlines = [ControlImagesInline]
    list_display = ('patient', 'date', 'details')

    class ControlImagesInline(admin.TabularInline):
        model = Control_Images
        extra = 1

admin.site.register(AdminManagedUser, AdminManagedUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientImage, PatientImageAdmin)
admin.site.register(Control, ControlAdmin)
