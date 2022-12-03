# from .views import GoogleLoginView,EmailPasswordLoginView,UserDetails,EmailPasswordSignupView,EmailVerificationApi
from .views.google_signin import GoogleLoginView
from django.urls import path,include

urlpatterns = [
    path('v1/login/google/', GoogleLoginView.as_view()),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth2/', include('djoser.urls.authtoken')),
    # path('v1/login/email/', EmailPasswordLoginView.as_view()),
    # path('v1/signup/email/', EmailPasswordSignupView.as_view()),
    # path('v1/signup/verify/', EmailVerificationApi.as_view(), name="email_verification"),
    # path('v1/profile/', UserDetails.as_view()),
]
