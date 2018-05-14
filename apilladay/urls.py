from django.contrib import admin
from django.urls import path, include

from default.views import LoginView, LogoutView
from users.views import DoctorRegistrationView, PatientRegistrationView
from response.views import arduino, MobileResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/doctor', DoctorRegistrationView.as_view(), name='doctor-register'),
    path('register/patient', PatientRegistrationView.as_view(), name='patient-register'),
    path('dashboard/', include('dashboard.urls')),
    path('response/box/<int:pid>', arduino, name='arduino-response'),
    path('response/app/<int:pid>', MobileResponse.as_view(), name='mobile-response')

]

