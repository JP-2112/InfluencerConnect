from django.contrib import admin
from .models import Conversation, ConversationMessage

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'updated_at', 'get_participants')
    list_filter = ('updated_at',)
    search_fields = ('participants__username',)
    
    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participantes'

@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'content')
    date_hierarchy = 'timestamp'

