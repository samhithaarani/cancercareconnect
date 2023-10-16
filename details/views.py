# details/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Patient 
from django.db.models import Q,Count
import matplotlib.pyplot as plt
import os
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage




class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('patients_info')
        return super().get_success_url()
# views.py

import matplotlib
matplotlib.use('Agg')  # Use Agg backend to generate images without displaying them

# Import other necessary modules

# Define a function to generate and save the pie chart image
@login_required

def generate_pie_chart(request):
    # Retrieve all patients
    patients = Patient.objects.all()

    # Generate data for the pie chart
    primary_tumor_counts = patients.values('primary_tumor').annotate(count=Count('primary_tumor')).order_by('-count')

    total_patients = patients.count()

    labels = [f"{item['primary_tumor']} ({item['count']} - {item['count']/total_patients*100:.2f} %)" for item in primary_tumor_counts]
    counts = [item['count'] for item in primary_tumor_counts]

    # Create the pie chart with counts and labels
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=labels, startangle=140, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Distribution of Primary Tumors')

    # Save the chart as an image in the static directory
    dest_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'pie_chart.png')
    plt.savefig(dest_image_path, bbox_inches='tight', pad_inches=0.2)  # Adjust parameters as needed
    plt.close()  # Close the figure
    return render(request, 'stats.html', {'chart_image_path': 'pie_chart.png',})
# Define your view function
@login_required
def patients_info(request):
    search_query = request.GET.get('search', '')
    study = request.GET.get('study', '')

    # Start with all patients
    patients = Patient.objects.all()

    # Apply the study filter
    if study == '1':
        patients = patients.filter(mark_for_study=True)
        show_back_to_info = True 
    else:
        show_back_to_info = False

    # Apply the search filter
    if search_query:
        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(primary_tumor__icontains=search_query)
        )

    # Create a Paginator object with the patients queryset and the desired number of items per page
    items_per_page = 10  # Adjust as needed
    paginator = Paginator(patients, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'patients_info.html', {
        'page': page,
        'user': request.user,
        'search_query': search_query,
        'study_filter': study,  # Pass the study filter to the template
        'chart_image_path': 'pie_chart.png',
        'patients': patients,  # Pass the patients queryset to the template
        'show_back_to_info': show_back_to_info,
    })
@login_required
def patient_detail(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    return render(request, 'patient.html', {'patient': patient})

def redirect_authenticated_user(request):
    if request.user.is_authenticated:
        return redirect('patients_info')
    else:
        return redirect('login')




