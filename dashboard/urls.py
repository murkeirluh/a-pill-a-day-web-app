from django.urls import path, include, re_path
from django.contrib import admin

from dashboard.views import DashboardHome, PrescriptionView, AddPrescriptionView, ScheduleView, AddScheduleView, DeletePrescriptionView, UserUpdateView

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard'),
    path('update-profile/', UserUpdateView.as_view(), name='update-profile'),
    path('update/prescription-<int:pid>', PrescriptionView.as_view(), name='update-prescription'),
    path('add/prescription', AddPrescriptionView.as_view(), name='add-prescription'),
    path('delete/prescription', DeletePrescriptionView.as_view(), name='delete-prescription'),
    path('schedules-<int:sched_id>/', ScheduleView.as_view(), name='view-schedule'),
    path('add/schedule', AddScheduleView.as_view(), name='add-schedule')

]