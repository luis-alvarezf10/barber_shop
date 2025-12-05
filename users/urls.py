from django.urls import path
from . import views

app_name = 'users' 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # TEMPORAL: Eliminar después de crear el primer admin
    path('setup-admin/', views.create_first_admin, name='setup_admin'),
]