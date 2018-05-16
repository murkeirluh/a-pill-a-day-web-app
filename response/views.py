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

from datetime import datetime, time, timezone

morn_start = time(0,0)
aft_start = time(12,0)
eve_start = time(18,0)
eve_end = time(23,59)
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def generate_output(day, time_):
    # matrix = [[0 for i in range(7)] for i in range(3)]
    d = days.index(day)
    t = 0
    if time_ >= morn_start and time_ < aft_start:
        t = 1
    elif time_ >= aft_start and time_ < eve_start:
        t = 2
    elif time_ >= eve_start and time_ < eve_end:
        t = 3
    
    return d,t


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def localize(dt):
    return dt.astimezone(tz=None)


def arduino(request, pid):
    content = ""
    current_time = datetime.now()
    curr_time = datetime.now()
    # display_text = current_time.strftime('%H:%M:%S %B %d, %Y')
    # code_text = current_time.strftime('%H,%M,%S,%d,%m,%y')
    light = False

    day = curr_time.strftime('%A')
    time_ = curr_time.strftime('%H:%M:%S')
    
    # five minutes before current time
    try:
        before = time(current_time.hour, current_time.minute - 5)
    except ValueError:
        before = time((current_time.hour - 1) % 24 , (current_time.minute - 5) % 60)
    
    # five minutes after current time
    try:
        after = time(current_time.hour, current_time.minute + 5)
    except ValueError:
        after = time((current_time.hour + 1) % 24 , (current_time.minute + 5) % 60)
    
    current_time = localize(datetime.now())

    # find schedule within -5 and +5 minutes of current time
    schedules = Schedules.objects.filter(presc__patient__patient_id=pid, day=day, time__gte=before, time__lte=after)
    # get the list of schedule times
    schedule_times = list(schedules.values_list('time', flat=True))

    # if there are schedules within the last and next five minutes
    if schedule_times:
        # light up
        light = True
        intake_times = list(Intakes.objects.all().values_list('time_taken', flat=True))
        today = datetime.today()
        
        for s in range(len(schedule_times)):
            schedule_times[s] = localize(datetime.combine(today, schedule_times[s]))

        for i in range(len(intake_times)):
            intake_times[i] = utc_to_local(intake_times[i])
            # if there was an intake between the schedule time and current time
            if intake_times[i] >= min(schedule_times) and intake_times[i] <= current_time:
                # light should be off
                light = False
                break
    
    # output: (<day_index:int>, <time_index:int>) <light_up:bool>
    # where day_index = 0 - Sunday, 1 - Monday, ... 6 - Saturday
    # time_index = 1 - Morning, 2 - Afternoon, 3 - Evening
    content += str(generate_output(day, time(current_time.hour, current_time.minute)))
    content += (" " + str(light))
            
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
        # format = '%Y-%m-%dT%H:%M:%S.%fZ'
        # date = datetime.strptime(data['time_taken'], format)
        # data['time_taken'] = date
        # print (data['time_taken'])
        print(data)
        serializer = IntakeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
        






