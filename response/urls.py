from django.urls import path, include, re_path
from django.contrib import admin

import views

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard'),
    path('update-profile/', UserUpdateView.as_view(), name='update-profile'),

]