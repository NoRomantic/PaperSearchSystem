from django.urls import path
from process_form import views


app_name = 'processform'
urlpatterns = [
    path('home/', views.home, name='home_html'),
    path('about/', views.about, name='about_html'),
    path('search/', views.search, name='search_html'),
    path('result/', views.result, name='result_html'),
]
