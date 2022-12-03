from django.contrib import admin
from django.urls import path, include
from .views import FcmTokenUpdateView

urlpatterns = [
    path('token/', FcmTokenUpdateView.as_view())

]
