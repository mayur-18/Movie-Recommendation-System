from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommendation/', views.recommendation, name='recommendation'),  # Define the URL pattern for 'recommendation'
]
