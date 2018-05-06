from django.shortcuts import render, redirect
from django.views.generic import (View, DetailView)
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

class LoginView(TemplateView):
    template_name = 'default/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # return redirect(reverse('dashboard'))
                return HttpResponse("Successfully logged in as %s" % user.username)
            else:
                messages.error(request, 'Login failed')
                return self.get(request)
        except:
            messages.error(request, 'Login failed')
            return self.get(request)