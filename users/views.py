from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import random_username, Doctors, Patients
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse

User = get_user_model()

""" View for doctor registering for an account or 
    admin creating account for doctor """
class DoctorRegistrationView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'auth/doctor_reg.html'

        rand_username = random_username

        while User.objects.filter(username=rand_username).first():
            rand_username = random_username

        context = {
            'random_username': rand_username
        }

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        new_doctor = {}

        username = request.POST.get('username')
        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        password = request.POST.get('password')

        new_doctor = Doctors.objects.create_doctor(
            username=username, 
            password=password,
            name=name, 
            specialization=specialization,
        )

        context = {
            'new_user': new_doctor
        }

        messages.success(request, 'Profile created. Please log in')
        
        return redirect(reverse('login'))
        

""" View for doctor creating patient account """
class PatientRegistrationView(LoginRequiredMixin, DetailView):
    template_name = 'auth/patient_reg.html'

    def get(self, request, *args, **kwargs):
        """ Generate a key upon loading view """
        # genkey = generate_key()
        rand_username = random_username

        while User.objects.filter(username=rand_username).first():
            rand_username = random_username
        
        context = {
            'random_username': rand_username,
            'doctor_id': self.request.user.doctor_id
        }
        
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        new_patient = {}

        username = request.POST.get('username')
        password = request.POST.get('password')
        doctor_id = kwargs.get('doctor_id')
        name = request.POST.get('name')

        new_patient = Patients.objects.create_patient(
            username=username, 
            password=password,
            name=name, 
            doctor = doctor_id
        )

        context = {
            'new_user': new_patient
        }

        messages.success(request, 'Profile for patient created.')
        
        return redirect(reverse('dashboard'))




        

