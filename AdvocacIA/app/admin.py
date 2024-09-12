# admin.py
from django.contrib import admin
from .models import ChaveAcesso
from django.utils.crypto import get_random_string


class ChaveAcessoAdmin(admin.ModelAdmin):
    list_display = ['chave', 'is_used']
    actions = ['generate_new_keys']

    def generate_new_keys(self, request, queryset):
        for _ in range(2):  # Example: Generate 10 keys
            chave = ChaveAcesso(chave=get_random_string(50))
            chave.save()
        self.message_user(request, "2 novas chaves geradas com sucesso.")
    generate_new_keys.short_description = "Gerar novas chaves de acesso"

admin.site.register(ChaveAcesso, ChaveAcessoAdmin)
