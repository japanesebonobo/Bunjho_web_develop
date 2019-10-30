from django.urls import path
from . import views
 
app_name = 'bunjho_web_database'
urlpatterns = [
    path('index/', views.index_page, name='index_page'),
]