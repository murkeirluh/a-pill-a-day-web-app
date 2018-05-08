from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.models import Doctors, Patients

# prescriptions - id, doctor_id, patient_id, medicine, quantity, notes, date_created, date_modified

# schedules - id, prescription_id, time, day, medicine, quantity, notes, date_created, date_modified

class Prescriptions(models.Model):
    presc_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=100, null=False)
    # total quantity of medicines that patient will buy
    quantity = models.IntegerField(verbose_name="quantity", name="quantity", null=False)
    notes = models.TextField()
    date_created = models.DateField(default=timezone.now)
    date_modified = models.DateField(default=timezone.now)
    is_purchased = models.BooleanField(default=False)
    
    def __str__(self):
        return 'Prescription {}: {}, x{} ({})'.format(self.p, self.medicine, self.quantity, self.notes)

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
        return '{} at {}, {}'.format(self.medicine, self.time, self.day)

# intakes - id, patient_id, schedule_id, time_taken
class Intakes(models.Model):
    intake_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, primary_key=False, on_delete=models.CASCADE)
    sched = models.ForeignKey(Schedules, primary_key=False, on_delete=models.CASCADE)
    time_taken = models.TimeField(auto_now_add=True)