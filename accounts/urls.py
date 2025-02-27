from django.urls import path

from accounts import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('logout/', views.logout_view, name='logout'),
]
