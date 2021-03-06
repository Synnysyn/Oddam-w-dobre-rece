"""charitydonation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from charitydonationapp import (
    views as v,
)  # LandingPage, AddDonation, Login, Register, Info, UserSettings


router = routers.DefaultRouter()
router.register(r"institutions", v.InstitutionViewSet, basename="InstitutionViewSet")
router.register(r"categories", v.CategoryViewSet, basename="CategoryViewSet")
router.register(r"institutions-1", v.InstitutionFundViewSet)
router.register(r"institutions-2", v.InstitutionOrgViewSet)
router.register(r"institutions-3", v.InstitutionEarnViewSet)


urlpatterns = [
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", v.LandingPage.as_view(), name="index"),
    path("donation/", v.AddDonation.as_view(), name="donation"),
    path("login/", v.Login.as_view(), name="login"),
    path("register/", v.Register.as_view(), name="register"),
    path("info/", v.Info.as_view(), name="info"),
    path("settings/", v.UserSettings.as_view(), name="settings"),
    path("", include(router.urls)),
]
