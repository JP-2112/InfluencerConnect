from django.urls import path
from . import views
from .views import (
    create_profile, edit_profile, ProfileDetailView,
    CompanyListView, InfluencerListView
)

app_name = 'profiles'

urlpatterns = [
    path('create/<str:user_type>/', create_profile, name='create_profile'),
    path('edit/', edit_profile, name='edit_profile'),
    path('detail/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('influencers/', InfluencerListView.as_view(), name='influencer_list'),
    path('view/', views.view_profile, name='view_profile'),
]

