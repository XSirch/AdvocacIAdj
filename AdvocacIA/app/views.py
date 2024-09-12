from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, DocumentoForm, ProfileForm
from .models import Documento, Profile
from .utils import gerar_e_verificar_documento

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm(request)
    return render(request, 'login.html', {'form': form})

def cadastro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Por favor, faça login.')
            
            return redirect('login')  # Redirect to login page
        else:
            print(form.errors)
            messages.error(request, 'Erro no cadastro. Por favor, verifique as informações fornecidas.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'cadastro.html', {'form': form})

@login_required
def admin_view(request):
    if not request.user.is_admin:
        return redirect('documento')
    # Implemente as funcionalidades de administrador aqui
    return render(request, 'admin.html')

@login_required
def minha_conta(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('minha_conta')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'minha_conta.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def documentos_view(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            servico = form.cleaned_data['servico']
            data = form.cleaned_data['data']
            detalhes = form.cleaned_data['detalhes']

            if 'regenerate' in request.POST:
                # Se o usuário solicitar uma nova geração com sugestões adicionais
                original_prompt = request.POST['original_prompt']
                additional_suggestions = request.POST['additional_suggestions']
                # Combinar o prompt original com novas sugestões
                new_prompt = f"{original_prompt} Considere também as seguintes sugestões: {additional_suggestions}"
                documento_gerado, verificacao, _ = gerar_e_verificar_documento(cliente, servico, data, detalhes)
            else:
                # Geração e verificação do documento pela primeira vez
                documento_gerado, verificacao, original_prompt = gerar_e_verificar_documento(cliente, servico, data, detalhes)

            if "Aprovada" in verificacao:
                # Se a verificação for aprovada, salvar o documento no banco de dados
                Documento.objects.create(
                    cliente=cliente,
                    servico=servico,
                    data=data,
                    detalhes=detalhes,
                    documento=documento_gerado,
                )
                return redirect('documento')
            else:
                # Se a verificação não for aprovada, exibir o documento gerado e a verificação
                return render(request, 'documento.html', {
                    'form': form,
                    'verificacao': verificacao,  # Exibe o feedback da verificação
                    'documento_gerado': documento_gerado,  # Documento para revisão
                    'original_prompt': original_prompt,  # Manter o prompt original
                    'additional_suggestions': '',  # Campo para sugestões adicionais
                })
    else:
        form = DocumentoForm()

    documentos = Documento.objects.all()
    return render(request, 'documento.html', {'form': form, 'documento': documentos})
