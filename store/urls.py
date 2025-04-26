
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
	path('', views.store, name="store"),
    path('movie/<int:id>/', views.movie_detail, name='movie_detail'),
        
    path('login/', views.custom_login, name='custom_login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),

    path('rent/<int:movie_id>/', views.rent_movie, name='rent_movie'),
    path('return/<int:movie_id>/', views.return_movie, name='return_movie'),
]

