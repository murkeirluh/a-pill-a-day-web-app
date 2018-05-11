from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse
from django.db.utils import IntegrityError
from random import choice

from users.models import random_username, Doctors, Patients

User = get_user_model()

def generate_key():
    chars = [chr(i) for i in range(ord('a'), ord('z')+1)]
    chars.extend([chr(i) for i in range(ord('A'), ord('Z')+1)])
    chars.extend([str(i) for i in range(10)])
    key = ''

    for i in range(6):
        key += choice(chars)

    return key

""" View for doctor registering for an account or 
    admin creating account for doctor """
class DoctorRegistrationView(View):
    def get(self, request, *args, **kwargs):

        template_name = 'auth/doctor_reg.html'
        if self.request.user.is_anonymous or self.request.user.user_type == 'admin':

            rand_username = random_username

            while User.objects.filter(username=rand_username).first():
                rand_username = random_username

            context = {
                'random_username': rand_username
            }

            return render(request, template_name, context)
        else:
            messages.error(request, "You are unauthorized to view this page.")
            return redirect(reverse('home'))

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
    def get(self, request, *args, **kwargs):
        template_name = 'auth/patient_reg.html'
        
        if self.request.user.user_type == 'doctor':
            doctor = Doctors.objects.get(user__user_id=self.request.user.user_id)
            context = {
                'doctor_id': doctor.doctor_id,
                'key': generate_key()
            }
            
            return render(request, template_name, context)
        else:
            messages.error(request, "You are unauthorized to view this page.")
            return redirect(reverse('home'))

    def post(self, request, *args, **kwargs):
        try:
            print("PUMASOK")
            new_patient = {}

            username = request.POST.get('username')
            doctor_id = request.POST.get('doctor_id')
            name = request.POST.get('name')
            key = request.POST.get('key')
            print("PUMASOK")
            new_patient = Patients.objects.create_patient(
                username=username, 
                password=key,
                name=name, 
                doctor = Doctors.objects.get(doctor_id=doctor_id),
                key=key
            )

            context = {
                'new_user': new_patient
            }

        except IntegrityError:
            messages.error(request, "That username is taken.")
            return redirect(reverse('patient-register'))


        else:
            messages.success(request, 'Profile for patient created.')
            return redirect(reverse('dashboard'))

class UserUpdateView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/update_profile.html'

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        old_username = request.POST.get('old_username')
        old_name = request.POST.get('old_name')
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        old_password = request.POST.get('old_password')

        user = get_object_or_404(User, username=old_username)
        patient = Patients.objects.get(name=old_name)

        if user.check_password(old_password):
            try:
                user.username = username
                user.set_password(password)
                user.save()
            except ObjectDoesNotExist:
                pass 
            except:
                messages.error(request, 'There was a problem updating your profile.')
            messages.success(request, 'Successfully updated profile.')
            
        else:
            messages.error(request, 'The password you entered was incorrect.')
        return redirect(reverse('dashboard'))





        

