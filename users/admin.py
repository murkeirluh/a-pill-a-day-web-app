from django.contrib import admin
from users.models import BaseUser, Administrators, Doctors, Patients

admin.site.register(BaseUser)
admin.site.register(Administrators)
admin.site.register(Doctors)
admin.site.register(Patients)

