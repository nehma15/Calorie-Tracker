from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('bmi/', views.bmi, name='bmi'),
    path('index/', views.index, name='index_page'),          
    path('delete/<int:id>/', views.delete_consume, name='delete'),
    path('save/', views.save_day, name='save_day'), 
    path('history/', views.history, name='history'),  
    path('delete_log/<int:id>/', views.delete_log, name='delete_log'),
]