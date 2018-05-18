from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.models import Doctors, Patients
from datetime import time

morn_start = time(0,0)
aft_start = time(12,0)
eve_start = time(18,0)
eve_end = time(23,59)

class Prescriptions(models.Model):
    presc_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=100, null=False)
    # total quantity of medicines that patient will buy
    quantity = models.IntegerField(verbose_name="quantity", name="quantity", null=False)
    notes = models.TextField(blank=True)
    date_created = models.DateField(default=timezone.now)
    date_modified = models.DateField(default=timezone.now)
    is_purchased = models.BooleanField(default=False)
    
    def __str__(self):
        return '{} x{} ({})'.format(self.medicine, self.quantity, self.notes)

class Schedules(models.Model):
    sched_id = models.AutoField(primary_key=True)
    presc = models.ForeignKey(Prescriptions, on_delete=models.CASCADE)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=False)
    day = models.CharField(max_length=10, null=False)
    medicine = models.CharField(max_length=100, null=False)
    quantity = models.IntegerField(verbose_name="quantity", name="quantity", null=False)
    date_created = models.DateField(default=timezone.now)
    date_modified = models.DateField(default=timezone.now)

    def __str__(self):
        return 'x{} {} at {}, {}'.format(self.quantity, self.medicine, self.time, self.day)

    def get_str(self):
        string = "x" + str(self.quantity) + " " + str(self.medicine)
        string += " for " + str(self.day)
        if self.time >= morn_start and self.time < aft_start:
            string += " morning"
        elif self.time >= aft_start and self.time < eve_start:
            string += " afternoon"
        elif self.time >= eve_start and self.time < eve_end:
            string += " evening"
        return string

# intakes - id, patient_id, schedule_id, time_taken
class Intakes(models.Model):
    intake_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, primary_key=False, on_delete=models.CASCADE)
    sched = models.ForeignKey(Schedules, primary_key=False, on_delete=models.CASCADE)
    time_taken = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} intake: sched {} at {}'.format(self.patient.name, self.sched.sched_id, self.time_taken)
