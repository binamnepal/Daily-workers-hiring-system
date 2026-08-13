from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import ServiceCategory
from .serializers import ServiceCategorySerializer


class ServiceCategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceCategorySerializer
    queryset = ServiceCategory.objects.filter(is_active=True)


class ServiceCategoryDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceCategorySerializer
    queryset = ServiceCategory.objects.filter(is_active=True)
    lookup_field = "slug"
