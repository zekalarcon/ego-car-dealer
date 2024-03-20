from django.urls import path
from login import views


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('logoutall/', views.LogoutAllView.as_view()),
]