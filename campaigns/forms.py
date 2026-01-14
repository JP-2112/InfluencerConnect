from django import forms
from .models import Campaign, Application, Response
from profiles.models import Category

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'deadline', 'budget', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),  # Mostrar categorías como botones
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu respuesta aquí...'}),
        }