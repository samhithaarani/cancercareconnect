# details/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.redirect_authenticated_user, name='index_redirect'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('patients/', views.patients_info, name='patients_info'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('generate_pie_chart/', views.generate_pie_chart, name='generate_pie_chart')

]
