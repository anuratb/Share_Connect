from django.urls import path
from . import views

from django.urls.conf import include
urlpatterns = [
    path('view-login/', views.ProfileListCreate.as_view() ),
    path('login/',views.handleLogin),
    path('',views.home),    
    path('home/',views.home),
    path('isLoggedIn/',views.isLoggedIn),
    path('logout/',views.logout),
    path('sign-up/',views.handleSignUp),
    path('reset/',include('django.contrib.auth.urls')),
    path('update-profile/',views.update_profile),
    path('profile/<username>/',views.profile),
    path('<username>/friends/',views.friends),
    path('blogs/<username>/',views.blogs),
    path('blogs/',views.blogs),
    path('search/',views.search)
]