from django import forms
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']  # Usa 'content' en lugar de 'body'
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe un mensaje'}),
        }

