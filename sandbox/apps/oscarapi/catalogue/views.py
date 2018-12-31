from django.conf import settings
from oscar.core.loading import get_model

from rest_framework import generics
from rest_framework import viewsets
from dynamic_rest.viewsets import DynamicModelViewSet, WithDynamicViewSetMixin
from .serializers import OptionSerializer, DynamicOptionSerializer, WithOptionSerializer

Option = get_model('catalogue', 'Option')


class OptionList(generics.ListAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class OptionDetail(generics.RetrieveAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class OptionViewSet(WithDynamicViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Option.objects.all()
    serializer_class = WithOptionSerializer


class DynamicOptionViewSet(WithDynamicViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Options API.
    """
    queryset = Option.objects.all()
    serializer_class = DynamicOptionSerializer
