from django import forms
from .models import Profile, CompanyProfile, InfluencerProfile, Category

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'website', 'location']  # Quitado 'profile_picture'
        labels = {
            'bio': 'Descripción',
            'website': 'Sitio web',
            'location': 'Ubicación',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'categories', 'company_size', 'description',
            'instagram_url', 'youtube_url', 'facebook_url', 'x_url'
        ]  # Quitado 'logo'
        widgets = {
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),
            'company_size': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/tuempresa'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/tuempresa'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/tuempresa'}),
            'x_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://x.com/tuempresa'}),
        }

class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = [
            'categories', 'platforms', 'audience_size', 'bio',
            'instagram_url', 'youtube_url', 'facebook_url', 'x_url'
        ]  # Quitado 'profile_photo'
        widgets = {
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}),
            'platforms': forms.TextInput(attrs={'class': 'form-control'}),
            'audience_size': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/tuusuario'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/tuusuario'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/tuusuario'}),
            'x_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://x.com/tuusuario'}),
        }

