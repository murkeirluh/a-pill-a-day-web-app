from django.db import models
from django.utils.text import slugify

# prescriptions - id, doctor_id, patient_id, medicine, quantity, notes, date_created, date_modified

class Prescriptions(models.Model):
    
    # p_id = 

    def __str__(self):
        pass