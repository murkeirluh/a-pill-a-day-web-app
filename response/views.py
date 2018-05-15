from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.decorators import method_decorator

from dashboard.models import Schedules, Intakes
from users.models import Patients
from dashboard.serializers import IntakeSerializer

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

    schedules = Schedules.objects.filter(presc__patient__patient_id=pid, day=day, time=time)

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
    
""" RETURN LOGINREQUIREDMIXIN ONCE LOGIN IS FIXED ON MOBILE APP """

@method_decorator(csrf_exempt, name='dispatch')
class MobileResponse(DetailView):
    @method_decorator(csrf_protect)
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
            # content = { 'error' : "You are unauthorized to view this page." }
            content = { 'error' : "An error occured." }
            return JsonResponse(content, status=400)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # app will send json object containing patient_id and sched_id
        data = JSONParser().parse(request)
        serializer = IntakeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
        






