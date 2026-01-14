from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    
    def get_success_url(self):
        return reverse_lazy('profiles:create_profile', kwargs={'user_type': self.object.user_type})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Autenticar y hacer login al usuario después de registrarse
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return response

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

@login_required
def company_list(request):
    companies = CustomUser.objects.filter(user_type='empresa')
    return render(request, 'users/company_list.html', {'companies': companies})

@login_required
def influencer_list(request):
    influencers = CustomUser.objects.filter(user_type='influencer')
    return render(request, 'users/influencer_list.html', {'influencers': influencers})

