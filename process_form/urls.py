from django.urls import path
from process_form import views


app_name = 'processform'
urlpatterns = [
    path('home/', views.home, name='home_html'),
    path('about/', views.about, name='about_html'),
    path('search/', views.search, name='search_html'),
    path('result/', views.result, name='result_html'),
    path('edit/<forloop_counter>', views.edit, name='edit_html'),
    path('editunsearched/<forloop_counter>', views.edit_unsearched, name='edit_unsearched_html'),
    path('delete/<forloop_counter>', views.delete, name='delete_html'),
    path('deleteunsearched/<forloop_counter>', views.delete_unsearched, name='delete_unsearched_html'),
    path('paperinfo/', views.paperinfo, name='paperinfo_html'),
    path('add/', views.add, name='add_html'),
    path('research/<forloop_counter>', views.research, name='research_html'),
    path('nofile/', views.nofile, name='nofile_html'),
    path('addinfo/<forloop_counter>', views.addinfo, name='add_info'),
]
