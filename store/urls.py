
from django.urls import path

from . import views

urlpatterns = [
	path('', views.store, name="store"),
    path('movie/<int:id>/', views.movie_detail, name='movie_detail'),

]