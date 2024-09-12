from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Documento, Profile, ChaveAcesso

class CustomUserCreationForm(UserCreationForm):
    chave_acesso = forms.CharField(max_length=50, label='Chave de Acesso')
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'chave_acesso', 'password1', 'password2', 'chave_acesso']

    def clean_chave_acesso(self):
        chave_acesso = self.cleaned_data.get('chave_acesso')
        try:
            chave = ChaveAcesso.objects.get(chave=chave_acesso, is_used=False)
        except ChaveAcesso.DoesNotExist:
            raise forms.ValidationError("Chave de acesso inválida ou já usada.")
        return chave_acesso
    
    def save(self, commit=True):
        user = super().save(commit=False)
        chave_acesso = self.cleaned_data.get('chave_acesso')
        chave = ChaveAcesso.objects.get(chave=chave_acesso)
        chave.is_used = True  # Mark the key as used
        chave.save()
        user.chave_acesso = chave_acesso  # Assign the key to the user
        if commit:
            user.save()
        return user
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['chave_acesso'].widget.attrs.update({'class': 'form-control'})

     # Adding help text for password fields
        self.fields['password1'].help_text = (
            "Sua senha precisa ter pelo menos 8 caracteres, "
            "não pode ser inteiramente numérica, "
            "e não pode ser uma senha comum."
        )
        self.fields['password2'].help_text = "Insira a mesma senha novamente para confirmação."

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nome de Usuário",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("Essa conta está inativa.", code='inactive')

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento  # Assuming Documento is a model in your app
        fields = ['cliente', 'servico', 'data', 'detalhes']  # Replace with actual field names

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']

    