from django.db import models
from django.conf import settings
from django.utils.timezone import now
from profiles.models import Category  # Importar el modelo de categorías

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'empresa'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_campaigns')
    categories = models.ManyToManyField(Category, blank=True, related_name='campaigns')  # Relación con categorías

    def __str__(self):
        return self.name

    def is_active(self):
        return now() <= self.deadline

    def engagement_rate(self):
        if self.views > 0:
            return round(((self.likes + self.comment_set.count()) / self.views) * 100, 2)
        return 0.0

class Application(models.Model):
    campaign = models.ForeignKey(
        Campaign, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    influencer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'influencer'}
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.influencer.email} - {self.campaign.name}"

class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='comment_set'  # Cambia el related_name
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.campaign.name}"

class CampaignView(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='views_tracker'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.campaign.name}"

class Response(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respuesta de {self.user.username} a {self.application.campaign.name}"