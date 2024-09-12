from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('documento/', views.documentos_view, name='documento'),
    path('admin/', views.admin_view, name='admin'),
    path('logout/', views.logout_view, name='logout'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('', views.home_view, name='home'),
    #path('document-generation/', views.document_generation, name='document_generation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)