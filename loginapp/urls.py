from django.urls import path
from loginapp import views

urlpatterns = [
    path('',views.SignupPage,name="Signup"),
    path('login/',views.LoginPage,name="login"),
    path('dashboard/',views.Dashboardpage,name="dashboard"),
    path('logout/',views.Logout,name="logout"),
]
 