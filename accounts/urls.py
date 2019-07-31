from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns=[
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]