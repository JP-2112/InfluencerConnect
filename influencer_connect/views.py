from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from profiles.models import Profile, CompanyProfile, InfluencerProfile
from messages_app.models import Conversation

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido/a, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Email o contraseña inválidos.")
        else:
            messages.error(request, "Email o contraseña inválidos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Ahora completa tu perfil.")
            return redirect('profiles:create_profile', user_type=user.user_type)
        else:
            messages.error(request, "Error en el registro. Por favor, verifica la información.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('home')

@login_required
def dashboard_view(request):
    conversations = Conversation.objects.filter(participants=request.user)
    
    # Agregar el otro participante a cada conversación en el contexto
    for conversation in conversations:
        conversation.other_user = conversation.get_other_participant(request.user)

    context = {
        'conversations': conversations,
        'user': request.user,  # Asegurar que el usuario esté en el contexto
    }
    return render(request, 'dashboard.html', context)


