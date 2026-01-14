from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('empresa', 'Empresa'),
        ('influencer', 'Influencer'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']
    
    def __str__(self):
        return self.email

