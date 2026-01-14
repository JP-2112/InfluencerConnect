from django.contrib import admin
from .models import Profile, CompanyProfile, InfluencerProfile

class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    can_delete = False

class InfluencerProfileInline(admin.StackedInline):
    model = InfluencerProfile
    can_delete = False

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_type', 'location', 'date_created')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('user__user_type', 'date_created')
    
    def get_user_type(self, obj):
        return obj.user.user_type
    get_user_type.short_description = 'Tipo de usuario'
    
    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        if obj.user.user_type == 'empresa':
            return [CompanyProfileInline]
        else:  # influencer
            return [InfluencerProfileInline]

