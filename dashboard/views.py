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
            context['patients'] = Patients.objects.filter(doctor__user__username=current_user.username)
            context['schedules'] = Schedules.objects.filter(presc__doctor__user__username=current_user.username)
            context['prescriptions'] = Prescriptions.objects.filter(doctor__user__username=current_user.username)
            context['intakes'] = Intakes.objects.filter(patient__doctor__user__username=current_user.username)
        elif user_type == 'patient':
            context['schedules'] = Schedules.objects.filter(patient__user__username=current_user.username)
            context['prescriptions'] = Prescriptions.objects.filter(patient__user__username=current_user.username)
            context['intakes'] = Intakes.objects.filter(patient__user__username=current_user.username)
        elif user_type == 'admin':
            context['doctors'] = Doctors.objects.all()
            context['patients'] = Patients.objects.all()

        return context 

class PrescriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/prescriptions.html'

class AddPrescriptionView(LoginRequiredMixin, TemplateView):
    pass

class ScheduleView(LoginRequiredMixin, TemplateView):
    pass

class AddScheduleView(LoginRequiredMixin, TemplateView):
    pass