from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(pattern_name='categories:list', permanent=False)),
    path('accounts/', include('accounts.urls')),
    path('', include('categories.urls')),
    path('workers/', include('workers.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
]
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
