from django.db import models
from django.conf import settings

class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f'Conversación {self.id}'
    
    def get_last_message(self):
        return self.messages.order_by('-timestamp').first()
    
    def get_other_participant(self, user):
        return self.participants.exclude(id=user.id).first()

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f'Mensaje de {self.sender} en {self.conversation}'

