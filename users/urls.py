from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, CustomLoginView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('companies/', views.company_list, name='company_list'),
    path('influencers/', views.influencer_list, name='influencer_list'),
    
]

