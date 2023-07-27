from django.urls import path

from api.views import csv_save, top_5_customers


app_name = 'api'

urlpatterns = [
    path('csv/save/', csv_save, name='save'),
    path('csv/top-five/<str:filename>/', top_5_customers, name='top-five'),
]
