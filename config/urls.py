from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from accounts import views
from accounts.views import (
    AccountHomeRedirectView,
    HomePageView,
    dashboard_page,
    filter_page,
    index_page,
    mentor_chat,
)


def home_redirect(request):
    return redirect("/accounts/signup/")


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', HomePageView.as_view(), name='home'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', AccountHomeRedirectView.as_view(), name='account-home'),
    path('auth/registration/', include('accounts.urls')),
    path('api/mentor/', mentor_chat, name='mentor_chat'),
    path("", index_page, name="home"),
    path("filter/", filter_page, name="filter"),
    path("dashboard/", dashboard_page, name="dashboard"),
]
