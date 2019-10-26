from django.contrib import admin
from django.urls import path,include
from app1 import views
app_name='app1'
urlpatterns = [
    path('register',views.register,name='register'),
    path('login',views.user_login,name='login'),
    path('special',views.special,name='special'),
    path('logout',views.user_logout,name='logout'),
    path('search',views.user_search,name='search'),
    path('transaction',views.make_transaction,name='transaction'),
    path('profile',views.user_profile,name='profile'),
    path('viewprofile',views.user_profile_view,name='viewprofile'),
]