from django.contrib import admin
from django.urls import path, include

handler404 = 'backend.views.error_404'
handler500 = 'backend.views.error_500'
handler403 = 'backend.views.error_403'
handler400 = 'backend.views.error_400'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
]
