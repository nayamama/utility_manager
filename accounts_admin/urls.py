from django.urls import path

from . import views

app_name = 'accounts_admin'

urlpatterns = [
    path('sign_up/', views.UserCreateView.as_view(), name='sign-up'),
    path('index/', views.index, name='home'),
    path('login/', views.HomeView.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('update-profile/', views.ProfileUpdateView.as_view(), name='update-profile'),
    path('', views.root, name='root'),
]
