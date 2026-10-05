from django.urls import path
from . import views

app_name = 'assistant'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('checker/', views.checker_view, name='checker'),
    path('result/', views.result_view, name='result'),
    path('history/', views.history_view, name='history'),
    path('history/<int:check_id>/', views.history_detail_view, name='history_detail'),
    path('about/', views.about_view, name='about'),
]
