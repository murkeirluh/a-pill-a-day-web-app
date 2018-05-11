from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

User = get_user_model()

from users.models import Doctors, Patients, BaseUser
from dashboard.models import Schedules, Prescriptions, Intakes

# PrescriptionView, AddPrescriptionView, ScheduleView, AddScheduleView

class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        print(str(current_user), type(current_user), end="\n\n\n")
        user_type = current_user.user_type
        context = super(DashboardHome, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user

        if user_type == 'doctor':
            context['this_user'] = Doctors.objects.get(user__username=current_user.username)
            context['patients'] = Patients.objects.filter(doctor__user__username=current_user.username)
            context['schedules'] = Schedules.objects.filter(presc__doctor__user__username=current_user.username)
            context['prescriptions'] = Prescriptions.objects.filter(doctor__user__username=current_user.username)
            context['intakes'] = Intakes.objects.filter(patient__doctor__user__username=current_user.username)
        elif user_type == 'patient':
            context['this_user'] = Patients.objects.filter(user__username=current_user.username)
            context['schedules'] = Schedules.objects.filter(patient__user__username=current_user.username)
            context['prescriptions'] = Prescriptions.objects.filter(patient__user__username=current_user.username)
            context['intakes'] = Intakes.objects.filter(patient__user__username=current_user.username)
        elif user_type == 'admin':
            context['doctors'] = Doctors.objects.all()
            context['patients'] = Patients.objects.all()

        return context 


class PrescriptionView(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        template_name = 'dashboard/update_prescription.html'
        if self.request.user.user_type == 'doctor':
            presc_id = kwargs.get('pid')
            print(presc_id)
            doctor_id = Doctors.objects.get(user__user_id=self.request.user.user_id).doctor_id
            patients = Patients.objects.filter(doctor__doctor_id=doctor_id)
            try:
                prescription = Prescriptions.objects.get(presc_id=presc_id)

                if patients:  
                    context = {
                        'presc' : prescription,
                        'pid' : presc_id,
                        'patients' : patients,
                        'doctor_id' : doctor_id
                    }

                    kwargs ={
                        'pid': presc_id
                    }

                    return render(request, template_name, context)
                    
                else:
                    messages.error(request, "You have no patients to add prescriptions to.")
                    return redirect(reverse('home'))
            except:
                messages.error(request, "There was an error with fetching prescriptions.")
                return redirect(reverse('home'))

        else:
            messages.error(request, "You are unauthorized to view this page.")
            return redirect(reverse('home'))

    def post(self, request, *args, **kwargs):
        presc_id = self.request.POST.get('pid')
        doctor = Doctors.objects.get(user__user_id=self.request.user.user_id)
        patient_id = self.request.POST.get('patient_id')
        patient = Patients.objects.get(patient_id=patient_id)
        medicine = self.request.POST.get('medicine')
        quantity = int(request.POST.get('quantity'))
        notes = self.request.POST.get('notes') or None

        try:
            prescription = Prescriptions.objects.get(presc_id=presc_id)
            prescription.patient = patient
            prescription.medicine = medicine
            prescription.quantity = quantity
            if notes: 
                prescription.notes = notes

            prescription.save()
            messages.success(request, 'Updated prescription {} for {}'.format(presc_id, patient.name))

        except:
            messages.error(request, "There was a problem updating this prescription.")
        
        return redirect(reverse('home'))


class AddPrescriptionView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dashboard/add_prescription.html'
        if self.request.user.user_type == 'doctor':
            doctor_id = Doctors.objects.get(user__user_id=self.request.user.user_id).doctor_id
            patients = Patients.objects.filter(doctor__doctor_id=doctor_id)

            if patients:  
                context = {
                    'patients' : patients,
                    'doctor_id' : doctor_id
                }

                return render(request, template_name, context)
            else:
                messages.error(request, "You have no patients to add prescriptions to.")
                return redirect(reverse('home'))

        else:
            messages.error(request, "You are unauthorized to view this page.")
            return redirect(reverse('home'))


    def post(self, request, *args, **kwargs):
        doctor = Doctors.objects.get(user__user_id=self.request.user.user_id)
        patient_id = request.POST.get('patient_id')
        patient = Patients.objects.get(patient_id=patient_id)
        medicine = request.POST.get('medicine')
        quantity = int(request.POST.get('quantity'))
        notes = request.POST.get('notes') or None

        Prescriptions.objects.create(
            doctor=doctor,
            patient=patient,
            medicine=medicine,
            quantity=quantity,
            notes=notes
        )

        messages.success(request, 'Successfully added a prescription for {}'.format(patient.name))

        return redirect(reverse('dashboard'))

class AddPrescriptionView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dashboard/add_prescription.html'
        if self.request.user.user_type == 'doctor':
            doctor_id = Doctors.objects.get(user__user_id=self.request.user.user_id).doctor_id
            patients = Patients.objects.filter(doctor__doctor_id=doctor_id)

            if patients:  
                context = {
                    'patients' : patients,
                    'doctor_id' : doctor_id
                }

                return render(request, template_name, context)
            else:
                messages.error(request, "You have no patients to add prescriptions to.")
                return redirect(reverse('home'))

        else:
            messages.error(request, "You are unauthorized to view this page.")
            return redirect(reverse('home'))

class DeletePrescriptionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        presc_id = kwargs.get('pid') or self.request.GET.get('pid')
        
        try:
            prescription = Prescriptions.objects.get(presc_id=presc_id)
            prescription.delete()
            messages.success(request, 'Prescription {} successfully deleted'.format(presc_id))
        except:
            messages.error(request, "There was an error deleting that prescription.")
        return redirect(reverse('home'))

class ScheduleView(LoginRequiredMixin, TemplateView):
    pass

class AddScheduleView(LoginRequiredMixin, TemplateView):
    pass

class UserUpdateView(LoginRequiredMixin, TemplateView):
    pass