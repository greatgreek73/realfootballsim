from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home, name='home'),
    path('core/', include('core.urls')),
    path('clubs/', include(('clubs.urls', 'clubs'), namespace='clubs')),  # Добавление пространства имен 'clubs'
]
