"""apilladay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from default.views import LoginView, LogoutView
from users.views import DoctorRegistrationView, PatientRegistrationView
from response.views import arduino

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/doctor', DoctorRegistrationView.as_view(), name='doctor-register'),
    path('register/patient', PatientRegistrationView.as_view(), name='patient-register'),
    path('dashboard/', include('dashboard.urls')),
    path('response/box', arduino, name='arduino-response')
]

