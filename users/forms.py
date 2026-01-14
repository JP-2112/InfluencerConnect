from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Tipo de usuario"
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2', 'profile_picture')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nombre de usuario"
        self.fields['email'].label = "Correo electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = "Contraseña"

