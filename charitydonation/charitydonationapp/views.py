from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .models import Institution, Donation, Category
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def paginating(page, queryset):
    """
    use it to prepare paginated page from queryset
    """
    paginator = Paginator(queryset, 1)
    try:
        ref_dict = paginator.page(page)
    except PageNotAnInteger:
        ref_dict = paginator.page(1)
    except EmptyPage:
        ref_dict = paginator.page(paginator.num_pages)

    return ref_dict


class LandingPage(View):
    def get(self, request):
        institutions = Institution.objects.all().order_by("name")
        donations = Donation.objects.all()

        sack_count = 0
        organization_count = 0

        for institution in institutions:
            organization_count += 1
        
        for donation in donations:
            sack_count += donation.quantity
        
        page = request.GET.get("page", 1)
        dict_institutions = paginating(page, institutions)

        context = {
            "organization_count": organization_count,
            "sack_count": sack_count,
            "institutions": dict_institutions,
        }
        return render(request, "charitydonationapp/index.html", context)


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {
            "categories": categories,
            "institutions": institutions,
        }
        return render(request, "charitydonationapp/form.html", context)
    
    def post(self, request):
        quantity = request.POST["bags"]
        categories = request.POST["category"]
        raise Exception


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
    
    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        rep_password = request.POST["password2"]
        first_name = request.POST["name"]
        last_name = request.POST["surname"]
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            if password == rep_password:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
                login(request, user=user)
                return redirect("index")
        return redirect("register")

class Info(LoginRequiredMixin, View):
    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by("is_taken")
        context = {"donations":donations}
        return render(request, "charitydonationapp/info.html", context)
    
    def post(self, request):
        donation = Donation.objects.get(id = request.POST["donation_id"])
        if "donation_taken" in request.POST:
            donation.is_taken = True
        elif "donation_not_taken" in request.POST:
            donation.is_taken = False
        donation.save()
        return redirect("info")

class UserSettings(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "charitydonationapp/settings.html")
    
    def post(self, request):
        password = request.POST["password"]
        user = authenticate(request, username=request.user.username, password=password)
        if user is None:
            return redirect("settings")
        else:
            if "pass_change" in request.POST:
                new_password = request.POST["new_password"]
                new_password2 = request.POST["new_password2"]
                if new_password == new_password2:
                    user.set_password(new_password)
                    user.save()
                    login(request, user=user)
                    return redirect("info")
            
            elif "info_change" in request.POST:
                username = request.POST["username"]
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]

                if request.user.username == username:
                    user = User.objects.get(username=username)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    return redirect("info")
                else:
                    try:
                        User.objects.get(username=username)
                    except ObjectDoesNotExist:
                        user = User.objects.get(username=request.user.username)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.username = username
                        user.save()
                        return redirect("info")
                    return redirect("settings")
        return redirect("settings")