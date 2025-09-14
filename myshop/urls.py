from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect legacy or default profile URL to site root
    path('accounts/profile/', RedirectView.as_view(url='/', permanent=False)),
    path('', include('store.urls')),
]
