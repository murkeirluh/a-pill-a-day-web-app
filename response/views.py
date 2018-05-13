from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Schedules
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

def arduino(request):
    content = ""
    current_time = datetime.now()
    display_text = current_time.strftime('%H:%M:%S %B %d, %Y')
    code_text = current_time.strftime('%H,%M,%S,%d,%m,%y')

    day = current_time.strftime('%A')
    time = current_time.strftime('%H:%M:%S')

    schedules = Schedules.objects.filter(day=day, time=time)

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
    





