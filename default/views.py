from django.shortcuts import render, redirect
from django.views.generic import (View, DetailView)
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

from apilladay import settings

class LoginView(TemplateView):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))
            # return HttpResponse("You are logged in as %s" % request.user.username)
        else:
            return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard'))
                # return HttpResponse("Successfully logged in as %s" % user.username)
            else:
                messages.error(request, 'Your username or password was incorrect. Please try again.')
                return self.get(request)
        except:
            messages.error(request, 'Login failed. Please try again.')
            return self.get(request)

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        messages.success(request, 'You have successfully logged out')
        logout(request)
        return redirect(settings.LOGIN_URL)