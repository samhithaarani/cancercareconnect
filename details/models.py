from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower

class Patient(models.Model):
    SEX_CHOICES = [('M', 'Male'),('F', 'Female'),('O', 'Other'),]
    LUNG_CHOICES = [('L', 'Left Lung'), ('R', 'Right Lung') , ('B', 'Both Lungs')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    primary_tumor = models.CharField(max_length=100)
    lung_option = models.CharField(max_length=1, choices=LUNG_CHOICES, blank=True, null=True)
    num_metastasis_left = models.PositiveIntegerField(blank=True, null=True)
    num_metastasis_right = models.PositiveIntegerField(blank=True, null=True)
    date_of_first_presentation = models.DateField(blank=True, null=True)
    ct_images_before = models.ManyToManyField('PatientImage', related_name='before_images', blank=True)
    ct_images_after = models.ManyToManyField('PatientImage', related_name='after_images', blank=True)
    mark_for_study = models.BooleanField(default=False)  # Add this field
    controls = models.ManyToManyField('Control', related_name='patient_controls', blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_case_insensitive_primary_tumor(cls, value):
        return cls.objects.filter(primary_tumor__iexact=value)

    @classmethod
    def get_case_insensitive_primary_tumor_containing(cls, substring):
        return cls.objects.filter(primary_tumor__icontains=substring)

    @classmethod
    def search_case_insensitive_primary_tumor(cls, value):
        return cls.objects.annotate(lower_primary_tumor=Lower('primary_tumor')).filter(lower_primary_tumor=value)

    @classmethod
    def search_case_insensitive_primary_tumor_containing(cls, substring):
        return cls.objects.annotate(lower_primary_tumor=Lower('primary_tumor')).filter(lower_primary_tumor__icontains=substring)

class PatientImage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ct_images/', blank=True)
    
    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - Image {self.id}"

class PatientAdditionalInfo(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    text_info = models.TextField()
    # Add more fields for images or other information

class Control(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.TextField()
    

    def __str__(self):
        return f"Control for {self.patient.first_name} {self.patient.last_name} on {self.date}"

class Control_Images(models.Model):
    control = models.ForeignKey(Control, on_delete=models.CASCADE, related_name='control_images_set')
    image = models.ImageField(upload_to='control/', blank=True)
    
    def __str__(self):
        return f"{self.control.patient.first_name} {self.control.patient.last_name} - Image {self.id}"


class AdminManagedUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=129)
    # ... (other fields)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        user = User.objects.create_user(username=self.username, password=self.password)
        super().save(*args, **kwargs)
