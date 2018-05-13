from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from datetime import time

User = get_user_model()

from users.models import Doctors, Patients, BaseUser
from dashboard.models import Schedules, Prescriptions, Intakes

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def validate_time(t_range, t):
    print(t_range, t)
    if t_range == 'morning':
        if t >= morn_start and t < aft_start:
            return True
        else:
            return False
    elif t_range == 'afternoon':
        if t >= aft_start and t < eve_start:
            return True
        else: return False

    elif t_range == 'evening':
        if t >= eve_start and t < eve_end:
            return True
        else: return False

'''
morning - [12am, 12nn) [00:00, 12:00)
afternoon - [12nn, 6pm) [12:00, 18:00) 
evening - [6pm, 12am) [18:00, 00:00) 

'''
morn_start = time(0,0)
aft_start = time(12,0)
eve_start = time(18,0)
eve_end = time(23,59)

# PrescriptionView, AddPrescriptionView, ScheduleView, AddScheduleView

class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        user_type = current_user.user_type
        schedules = Schedules.objects.filter(presc__doctor__user__username=current_user.username)
        context = super(DashboardHome, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user

        if user_type == 'doctor':
            context['this_user'] = Doctors.objects.get(user__username=current_user.username)
            context['patients'] = Patients.objects.filter(doctor__user__username=current_user.username).order_by('patient_id')
            context['prescriptions'] = Prescriptions.objects.filter(doctor__user__username=current_user.username).order_by('presc_id')
            context['intakes'] = Intakes.objects.filter(patient__doctor__user__username=current_user.username)
            context['schedules'] = {}

            morning = schedules.filter(time__gte=morn_start, time__lt=aft_start).order_by('time')
            afternoon = schedules.filter(time__gte=aft_start, time__lt=eve_start).order_by('time')
            evening = schedules.filter(time__gte=eve_start, time__lte=eve_end).order_by('time')
            
            for p in context['patients']:    
                context['schedules'][str(p.patient_id)] = { 'pid' : p.patient_id }
                context['schedules'][str(p.patient_id)]['schedules'] = {
                'monday' : {
                        'morning': morning.filter(presc__patient__patient_id=p.patient_id, day='Monday'),
                        'afternoon': afternoon.filter(presc__patient__patient_id=p.patient_id,day='Monday'), 
                        'evening': evening.filter(presc__patient__patient_id=p.patient_id,day='Monday')
                    },
                'tuesday' : {
                        'morning': morning.filter(presc__patient__patient_id=p.patient_id,day='Tuesday'), 
                        'afternoon': afternoon.filter(presc__patient__patient_id=p.patient_id,day='Tuesday'), 
                        'evening': evening.filter(presc__patient__patient_id=p.patient_id,day='Tuesday')
                    },
                'wednesday' : {
                        'morning': morning.filter(presc__patient__patient_id=p.patient_id,day='Wednesday'), 
                        'afternoon': afternoon.filter(presc__patient__patient_id=p.patient_id,day='Wednesday'), 
                        'evening': evening.filter(presc__patient__patient_id=p.patient_id,day='Wednesday')
                    },
                'thursday' : {
                        'morning': morning.filter(presc__patient__patient_id=p.patient_id,day='Thursday'), 
                        'afternoon': afternoon.filter(presc__patient__patient_id=p.patient_id,day='Thursday'), 
                        'evening': evening.filter(presc__patient__patient_id=p.patient_id,day='Thursday')
                    },
                'friday' : {
                        'morning': morning.filter(presc__patient__patient_id=p.patient_id,day='Friday'), 
                        'afternoon': afternoon.filter(presc__patient__patient_id=p.patient_id,day='Friday'), 
                        'evening': evening.filter(presc__patient__patient_id=p.patient_id,day='Friday')
                    },
                'saturday' : {
                        'morning': morning.filter(presc__patient__patient_id=p.patient_id,day='Saturday'), 
                        'afternoon': afternoon.filter(presc__patient__patient_id=p.patient_id,day='Saturday'), 
                        'evening': evening.filter(presc__patient__patient_id=p.patient_id,day='Saturday')
                    },
                'sunday' : {
                        'morning': morning.filter(presc__patient__patient_id=p.patient_id,day='Sunday'), 
                        'afternoon': afternoon.filter(presc__patient__patient_id=p.patient_id,day='Sunday'), 
                        'evening': evening.filter(presc__patient__patient_id=p.patient_id,day='Sunday')
                    }
                }
                    
        elif user_type == 'patient':
            context['this_user'] = Patients.objects.filter(user__username=current_user.username)
            context['schedules'] = Schedules.objects.filter(patient__user__username=current_user.username)
            context['prescriptions'] = Prescriptions.objects.filter(patient__user__username=current_user.username)
            context['intakes'] = Intakes.objects.filter(patient__user__username=current_user.username)
        elif user_type == 'admin':
            context['doctors'] = Doctors.objects.all()
            context['patients'] = Patients.objects.all()
        
        return render(request, self.template_name, context) 


class PrescriptionView(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        template_name = 'dashboard/update_prescription.html'
        if self.request.user.user_type == 'doctor':
            presc_id = kwargs.get('pid')
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
            patients = Patients.objects.filter(doctor__doctor_id=doctor_id).order_by('patient_id')

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
    def get(self, requests, *args, **kwargs):
        template_name = 'dashboard/add_schedule.html'
        if self.request.user.user_type == 'doctor':
            doctor_id = Doctors.objects.get(user__user_id=self.request.user.user_id).doctor_id
            time = self.request.GET.get('time') 
            day = self.request.GET.get('day')
            patient = self.request.GET.get('patient')
            
            if patient:
                prescriptions = Prescriptions.objects.filter(doctor__doctor_id=doctor_id, patient__patient_id=patient.patient_id)
                medicines = list(prescriptions.values_list('medicine', flat=True))
            else:
                prescriptions = Prescriptions.objects.filter(doctor__doctor_id=doctor_id).order_by('patient_id')
                medicines = list(prescriptions.values_list('medicine', flat=True))

            context = {
                'doctor_id' : doctor_id,
                'time' : time,
                'day' : day,
                'medicines' : medicines,
                'prescriptions': prescriptions
            }

            return render(request, template_name, context)

class AddScheduleView(LoginRequiredMixin, TemplateView):
    dictionary = {}
    patient = ''
    doctor_id = ''
    
    def get(self, request, *args, **kwargs):
        template_name = 'dashboard/add_schedule.html'
        if self.request.user.user_type == 'doctor':
            doctor_id = Doctors.objects.get(user__user_id=self.request.user.user_id).doctor_id
            self.doctor_id = doctor_id
            time = self.request.GET.get('time', kwargs.get('time'))
            day = self.request.GET.get('day', kwargs.get('day'))
            patient_id = self.request.GET.get('patient_id', kwargs.get('patient_id'))
            patient = (Patients.objects.filter(patient_id=patient_id).first() if patient_id else None)

            if patient_id:
                self.patient = Patients.objects.filter(patient_id=patient_id).first() or None
                prescriptions = Prescriptions.objects.filter(doctor__doctor_id=doctor_id, patient__patient_id=patient_id).order_by('presc_id')
                # medicines = list(prescriptions.values_list('medicine', flat=True))
            else:
                prescriptions = Prescriptions.objects.filter(doctor__doctor_id=doctor_id).order_by('patient_id')
                # medicines = list(prescriptions.values_list('medicine', flat=True))

            context = {
                'doctor_id' : doctor_id,
                'time' : time,
                'day' : day,
                'prescriptions': prescriptions
            }

            if patient:
                context['patient'] = patient
            if patient_id:
                context['patient_id'] = patient_id
            
            if len(self.dictionary) == 0:
                self.dictionary = context

            return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        patient = self.request.POST.get('patient')
        patient_id = self.request.POST.get('patient_id')
        presc_id = self.request.POST.get('prescription')
        prescription = Prescriptions.objects.get(presc_id=presc_id)
        medicine = self.request.POST.get('medicine')
        
        quantity = self.request.POST.get('quantity', 1)
        day = self.request.POST.get('day')
        seven_days = self.request.POST.get('seven_days', None)
        
        # repopulate dictionary
        self.dictionary['patient_id'] = self.request.POST.get('patient_id')
        self.dictionary['day'] = self.request.POST.get('day_arg')
        self.dictionary['time'] = self.request.POST.get('time_arg')

        try:
            time_ = self.request.POST.get('time')
            print("TIME:", time_)
            print("medicine:",medicine)
            print("day:",day)
            hour,minute = map(int, time_.split(':'))
            time_ = time(hour,minute)
        except TypeError as e:
            messages.error(request, e)
            print("incorrect format")
            return redirect(reverse('add-schedule')+'?patient_id=' + str(self.dictionary['patient_id']) + '&day=' + str(self.dictionary['day']) + '&time=' + str(self.dictionary['time']))
        # validate time input
        except Exception as e:
            messages.error(request, e)
            print("some error 1")
            print(self.dictionary)
            return redirect(reverse('add-schedule')+'?patient_id=' + str(self.dictionary['patient_id']) + '&day=' + str(self.dictionary['day']) + '&time=' + str(self.dictionary['time']))
        else:
            try:
                # if time submitted is in correct range
                if (validate_time(self.dictionary['time'], time_)):
                    # if checkbox was checked
                    if seven_days:
                        for d in days:
                            if len(Schedules.objects.filter(presc=prescription, day=d, time=time_, medicine=medicine, quantity=quantity)) == 0:
                                Schedules.objects.create(
                                    presc=prescription,
                                    time=time_,
                                    day=d,
                                    medicine=medicine,
                                    quantity=quantity
                                )
                    # if not checked                                
                    else:
                        try:
                            Schedules.objects.create(
                                presc=prescription,
                                time=time_,
                                day=day,
                                medicine=medicine,
                                quantity=quantity
                            )
                        except Exception:
                            messages.error(request, "There was an error adding a schedule.")
                            return redirect(reverse('home'))


                else:
                    messages.error(request, "Time not within the specified range.")
                    return redirect(reverse('add-schedule')+'?patient_id=' + str(self.dictionary['patient_id']) + '&day=' + str(self.dictionary['day']) + '&time=' + str(self.dictionary['time']))

                messages.success(request, "Successfully added schedule.")
                return redirect(reverse('home'))
            except Exception as e:
                messages.error(request, e)
                return redirect(reverse('add-schedule')+'?patient_id=' + str(self.dictionary['patient_id']) + '&day=' + str(self.dictionary['day']) + '&time=' + str(self.dictionary['time']))


               

class UserUpdateView(LoginRequiredMixin, TemplateView):
    pass


