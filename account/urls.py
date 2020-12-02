"""Создаем url"""
from django.urls import path
from account.views import RegisterView, LoginView, LogoutView, TokenRefresh, ActivationView

urlpatterns = [
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('login/refresh/', TokenRefresh.as_view()),
]

