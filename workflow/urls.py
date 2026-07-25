from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('demande/creer/', views.creer_demande, name='creer_demande'),
    path('demande/details', views.consulter_demande, name='consulter_demande'),
]
