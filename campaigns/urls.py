from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='campaign_list'),
    path('create/', views.campaign_create, name='campaign_create'),
    path('<int:campaign_id>/apply/', views.apply_to_campaign, name='apply_to_campaign'),
    path('<int:campaign_id>/applications/', views.campaign_applications, name='campaign_applications'),
    path('<int:campaign_id>/like/', views.like_campaign, name='like_campaign'),
    path('<int:application_id>/respond/', views.respond_to_application, name='respond_to_application'),
    path('influencer_applications/', views.influencer_applications, name='influencer_applications'),
    path('<int:campaign_id>/edit/', views.campaign_edit, name='campaign_edit'),
    path('', views.campaign_list, name='campaign_list'),
    path('<int:campaign_id>/comment/', views.add_comment, name='add_comment'),
]