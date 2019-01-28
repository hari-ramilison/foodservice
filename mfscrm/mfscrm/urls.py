"""mfscrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordChangeView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('crm.urls')),

    re_path(r'^accounts/login/$', LoginView.as_view(template_name='registration/login.html'), name="login"),
    re_path(r'^accounts/logout/$', LogoutView.as_view(template_name='registration/logged_out.html'), LogoutView.next_page, name="logout"),
    re_path(r'^accounts/password_reset/$', auth_views.PasswordResetView.as_view(template_name='registration/password_r_form.html'), name='password_reset'),
    re_path(r'^accounts/password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_r_done.html'), name='password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_r_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_r_complete.html'), name='password_reset_complete'),
]
