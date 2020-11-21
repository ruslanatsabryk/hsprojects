from django.shortcuts import render, redirect
from django.views import View
from .models import Resume
from django import forms
from django.http import HttpResponseForbidden

# Create your views here.
class Resumes(View):
    def get(self, request, *args, **kwargs):
        context = {'resumes': Resume.objects.all()}
        return render(request, 'resume/resumes.html', context)

class ResumeForm(forms.Form):
    description = forms.CharField(max_length=1024, label='Description')

class ResumeNew(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if not user.is_staff:
                resume_form = ResumeForm()
                context = {'resume_form': resume_form}
                return render(request, 'resume/resume_new.html', context)
            else:
                return HttpResponseForbidden()
        return redirect('/login')

    def post(self, request, *args, **kwargs):
        description = request.POST.get('description')
        user = request.user
        if user.is_authenticated:
            if not user.is_staff:
                Resume.objects.create(author=user, description=description)
                return redirect('/home')
            else:
                return HttpResponseForbidden()
        return redirect('/login')
