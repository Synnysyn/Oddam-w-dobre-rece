from django.shortcuts import render, redirect
from django.views import View
from .models import Institution, Donation
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class LandingPage(View):
    def get(self, request):
        institutions = Institution.objects.all()
        donations = Donation.objects.all()

        sack_count = 0
        organization_count = 0

        for institution in institutions:
            organization_count += 1
        
        for donation in donations:
            sack_count += donation.quantity

        context = {
            "organization_count": organization_count,
            "sack_count": sack_count,
            "institutions": institutions,
        }
        return render(request, "charitydonationapp/index.html", context)


class AddDonation(View):
    def get(self, request):
        return render(request, "charitydonationapp/form.html")


class Login(View):
    def get(self, request):
        return render(request, "charitydonationapp/login.html")
    
    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect("register")
        else:
            login(request, user=user)
            return redirect("index")


class Register(View):
    def get(self, request):
        return render(request, "charitydonationapp/register.html")