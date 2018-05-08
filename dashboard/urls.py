from django.urls import path, include
from django.contrib import admin

from dashboard.views import DashboardHome, PrescriptionView, AddPrescriptionView, ScheduleView, AddScheduleView


urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard'),

    path('prescriptions/<int:pid>/', PrescriptionView.as_view(), name='view-presc'),
    path('prescriptions/add/', AddPrescriptionView.as_view(), name='add-presc'),

    path('schedules/<int:sched_id>/', ScheduleView.as_view(), name='view-schedule'),
    path('schedules/add/', AddScheduleView.as_view(), name='add-schedule')

]