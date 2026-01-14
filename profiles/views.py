from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.contrib import messages
from .models import Profile, CompanyProfile, InfluencerProfile
from .forms import ProfileForm, CompanyProfileForm, InfluencerProfileForm
from users.models import CustomUser

@login_required
def create_profile(request, user_type):
    # Verificar que el tipo de usuario coincida con el del usuario autenticado
    if request.user.user_type != user_type:
        messages.error(request, "No tienes permiso para crear este tipo de perfil.")
        return redirect('dashboard')
    
    # Verificar si el usuario ya tiene un perfil
    try:
        profile = request.user.profile
        messages.info(request, "Ya tienes un perfil creado.")
        return redirect('dashboard')
    except Profile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        
        if user_type == 'empresa':
            specific_form = CompanyProfileForm(request.POST, request.FILES)
        else:  # influencer
            specific_form = InfluencerProfileForm(request.POST, request.FILES)
        
        if profile_form.is_valid() and specific_form.is_valid():
            # Crear perfil base
            profile = profile_form.save(commit=False)
            profile.user = request.user
            # No guardar foto de perfil subida por el usuario
            # if 'profile_picture' in request.FILES:
            #     profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            
            # Crear perfil específico
            specific_profile = specific_form.save(commit=False)
            specific_profile.profile = profile
            # No guardar logo ni foto de influencer subida por el usuario
            # if user_type == 'empresa' and 'logo' in request.FILES:
            #     specific_profile.logo = request.FILES['logo']
            # if user_type == 'influencer' and 'profile_photo' in request.FILES:
            #     specific_profile.profile_photo = request.FILES['profile_photo']
            specific_profile.save()
            
            # Guardar las categorías seleccionadas
            specific_form.save_m2m()  # Esto es necesario para ManyToManyField
            
            messages.success(request, "¡Tu perfil ha sido creado exitosamente!")
            return redirect('profiles:view_profile')
    else:
        profile_form = ProfileForm()
        
        if user_type == 'empresa':
            specific_form = CompanyProfileForm()
        else:  # influencer
            specific_form = InfluencerProfileForm()
    
    context = {
        'profile_form': profile_form,
        'specific_form': specific_form,
        'user_type': user_type
    }
    return render(request, 'profiles/create_profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile
    company_profile = getattr(profile, 'company', None)
    influencer_profile = getattr(profile, 'influencer', None)
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        # Actualizar datos del perfil base
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.website = request.POST.get('website', profile.website)
        # No permitir actualizar foto de perfil
        # if 'profile_picture' in request.FILES:
        #     profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        
        # Actualizar datos del perfil de empresa (si existe)
        if company_profile:
            company_form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile)
            if company_form.is_valid():
                # No permitir actualizar logo
                # if 'logo' in request.FILES:
                #     company_profile.logo = request.FILES['logo']
                company_form.save()
        
        # Actualizar datos del perfil de influencer (si existe)
        if influencer_profile:
            influencer_form = InfluencerProfileForm(request.POST, request.FILES, instance=influencer_profile)
            if influencer_form.is_valid():
                # No permitir actualizar foto de influencer
                # if 'profile_photo' in request.FILES:
                #     influencer_profile.profile_photo = request.FILES['profile_photo']
                influencer_form.save()
        
        return redirect('profiles:view_profile')  # Redirige a la página de perfil después de guardar
    
    # Renderizar el formulario con los datos actuales
    company_form = CompanyProfileForm(instance=company_profile) if company_profile else None
    influencer_form = InfluencerProfileForm(instance=influencer_profile) if influencer_profile else None
    
    return render(request, 'profiles/edit_profile.html', {
        'user': user,
        'profile': profile,
        'company_profile': company_profile,
        'influencer_profile': influencer_profile,
        'company_form': company_form,
        'influencer_form': influencer_form,
    })

@login_required
def view_profile(request):
    return render(request, 'profiles/view_profile.html', {
        'user': request.user,
        'company': getattr(request.user.profile, 'company', None),
        'influencer': getattr(request.user.profile, 'influencer', None),
    })

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

class CompanyListView(LoginRequiredMixin, ListView):
    model = CompanyProfile
    template_name = 'profiles/company_list.html'
    context_object_name = 'companies'
    
    def get_queryset(self):
        return CompanyProfile.objects.select_related('profile__user').all()

class InfluencerListView(LoginRequiredMixin, ListView):
    model = InfluencerProfile
    template_name = 'profiles/influencer_list.html'
    context_object_name = 'influencers'
    
    def get_queryset(self):
        return InfluencerProfile.objects.select_related('profile__user').all()

