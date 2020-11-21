from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

class Menu(View):
    def get(self, request, *args, **kwargs):
        context = dict()
        return render(request, 'hyperjob/menu.html', context)

class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/login'
    template_name = 'hyperjob/signup.html'

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'hyperjob/login.html'

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff and request.user.is_authenticated:
            return redirect('/vacancy/new')
        elif not request.user.is_staff and request.user.is_authenticated:
            return redirect('/resume/new')
        return redirect('/login')