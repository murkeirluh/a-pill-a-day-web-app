from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from dashboard.models import Schedules
from users.models import Patients
from datetime import datetime, time

morn_start = time(0,0)
aft_start = time(12,0)
eve_start = time(18,0)
eve_end = time(23,59)
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def generate_matrix(day=None, time=None):
    matrix = [[0 for i in range(7)] for i in range(3)]
    if day and time:
        d = days.index(day)
        t = 0
        if time >= morn_start and time < aft_start:
            t = 0
        elif time >= aft_start and time < eve_start:
            t = 1
        elif time >= eve_start and time < eve_end:
            t = 2

        matrix[d][t] = 1    
    
    print (matrix)
    return matrix

def arduino(request, pid):
    content = ""
    current_time = datetime.now()
    display_text = current_time.strftime('%H:%M:%S %B %d, %Y')
    code_text = current_time.strftime('%H,%M,%S,%d,%m,%y')

    day = current_time.strftime('%A')
    time = current_time.strftime('%H:%M:%S')

    schedules = Schedules.objects.filter(presc__patient_patient_id=pid, day=day, time=time)

    content += "Current time: "
    content += display_text
    content += '\n'
    content += code_text
    content += "\n\n"

    if len(schedules):
        matrix = generate_matrix(day, time)
    else:
        matrix = generate_matrix()

    content += '['
    for m in range(len(matrix)):
        content += str(matrix[m])
        if m != len(matrix)-1: 
            content += '\n'
    content += ']'

    return HttpResponse(content, content_type='text/plain')
    
class MobileResponse(DetailView):
    
    def get(self, request, *args, **kwargs):
        pid = kwargs.get('pid')
        patient_id = kwargs.get('pid')
        patient = Patients.objects.get(patient_id=patient_id)
        # current_user = self.request.user
        # if self.request.user == patient.user:

        if patient:
            s = Schedules.objects.filter(presc__patient__patient_id=pid).order_by('sched_id')
            schedules = list(s.values())
            json_list = { 'schedules' : schedules }

            return JsonResponse(json_list, safe=False)
        else:
            content = "You are unauthorized to view this page."
            return HttpResponse(content, content_type='text/plain')
        






