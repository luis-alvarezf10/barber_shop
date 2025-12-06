from django.urls import path
from . import views

app_name = 'users' 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('employees/', views.employees_view, name='employees'),
    path('employees/add/', views.add_employee_view, name='add_employee'),
]