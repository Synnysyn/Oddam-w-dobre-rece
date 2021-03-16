from django.shortcuts import render
from django.views import View

# Create your views here.


class LandingPage(View):
    def get(self, request):
        return render(request, "charitydonationapp/index.html")


class AddDonation(View):
    def get(self, request):
        return render(request, "charitydonationapp/form.html")


class Login(View):
    def get(self, request):
        return render(request, "charitydonationapp/login.html")


class Register(View):
    def get(self, request):
        return render(request, "charitydonationapp/register.html")