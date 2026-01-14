from django.db import models
from django.conf import settings
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='images/', default='images/descargar.png')  # Ajuste en la ruta predeterminada
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_absolute_url(self):
        return reverse('profiles:profile_detail', kwargs={'pk': self.pk})

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CompanyProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='company')
    categories = models.ManyToManyField('Category', blank=True, related_name='companies')
    company_size = models.CharField(max_length=10, choices=(
        ('1-10', '1-10 empleados'),
        ('11-50', '11-50 empleados'),
        ('51-200', '51-200 empleados'),
        ('201-500', '201-500 empleados'),
        ('501+', '501+ empleados'),
    ))
    logo = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(blank=True)
    instagram_url = models.URLField("Instagram URL", blank=True, null=True)
    youtube_url = models.URLField("YouTube URL", blank=True, null=True)
    facebook_url = models.URLField("Facebook URL", blank=True, null=True)
    x_url = models.URLField("X (Twitter) URL", blank=True, null=True)

    def __str__(self):
        return f'{self.profile.user.username} Company Profile'

class InfluencerProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='influencer')
    categories = models.ManyToManyField('Category', blank=True, related_name='influencers')
    platforms = models.CharField(max_length=200, blank=True)
    audience_size = models.CharField(max_length=10, choices=(
        ('micro', 'Micro (1K-10K seguidores)'),
        ('pequeno', 'Pequeño (10K-50K seguidores)'),
        ('medio', 'Medio (50K-100K seguidores)'),
        ('grande', 'Grande (100K-500K seguidores)'),
        ('macro', 'Macro (500K-1M seguidores)'),
        ('mega', 'Mega (1M+ seguidores)'),
    ))
    profile_photo = models.ImageField(upload_to='images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    instagram_url = models.URLField("Instagram URL", blank=True, null=True)
    youtube_url = models.URLField("YouTube URL", blank=True, null=True)
    facebook_url = models.URLField("Facebook URL", blank=True, null=True)
    x_url = models.URLField("X (Twitter) URL", blank=True, null=True)

    def __str__(self):
        return f'{self.profile.user.username} Influencer Profile'

