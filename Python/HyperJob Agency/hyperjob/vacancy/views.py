from django.shortcuts import render, redirect
from django.views import View
from .models import Vacancy
from django.http import HttpResponseForbidden

# Create your views here.
class Vacancies(View):
    def get(self, request, *args, **kwargs):
        context = {'vacancies': Vacancy.objects.all()}
        return render(request, 'vacancy/vacancies.html', context)


class VacancyNew(View):
    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                print('user.is_staff', user.is_staff)
                return render(request, 'vacancy/vacancy_new.html', context)
            else:
                return HttpResponseForbidden()
        return redirect('/login')

    def post(self, request, *args, **kwargs):
        description = request.POST.get('description')
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                print('user.is_staff', user.is_staff)
                Vacancy.objects.create(author=user, description=description)
                return redirect('/home')
            else:
                return HttpResponseForbidden()
        return redirect('/login')

