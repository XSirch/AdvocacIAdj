from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    chave_acesso = models.CharField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False)

    # Adding related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Change related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Change related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Documento(models.Model):
    cliente = models.CharField(max_length=255)
    servico = models.CharField(max_length=255)
    data = models.DateField()
    detalhes = models.TextField()
    documento = models.TextField()

    def __str__(self):
        return self.cliente

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pictures/', default='default_profile.png')


class ChaveAcesso(models.Model):
    chave = models.CharField(max_length=50, unique=True)  # Ensure unique keys
    is_used = models.BooleanField(default=False)  # Track if the key has been used

    def __str__(self):
        return self.chave

# Sinal para criar ou salvar o perfil automaticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()