from django.urls import path
from .views import inbox, conversation_detail, new_message

app_name = 'messages_app'

urlpatterns = [
    path('', inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('new/', new_message, name='new_message'),
]

