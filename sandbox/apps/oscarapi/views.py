from oscar.core.loading import get_model

from rest_framework import generics

from .serializers import OrderLineAttributeSerializer, OrderLineSerializer

from oscarapi.serializers import (
    CheckoutSerializer,
    OrderSerializer, UserAddressSerializer
)
from oscarapi.signals import oscarapi_post_checkout
from oscarapi.views.utils import parse_basket_from_hyperlink

Order = get_model('order', 'Order')
OrderLine = get_model('order', 'Line')
OrderLineAttribute = get_model('order', 'LineAttribute')


class OrderLineAttributeDetail(generics.RetrieveUpdateAPIView):
    queryset = OrderLineAttribute.objects.all()
    serializer_class = OrderLineAttributeSerializer


class OrderLineDetail(generics.RetrieveAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

    def get(self, request, pk=None, format=None):
        if not request.user.is_staff:
            self.queryset = self.queryset.filter(
                order__id=pk, order__user=request.user)

        return super(OrderLineDetail, self).get(request, format)


class OrderLineList(generics.ListAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

    def get(self, request, pk=None, format=None):
        if pk is not None:
            self.queryset = self.queryset.filter(
                order__id=pk, order__user=request.user)
        elif not request.user.is_staff:
            self.permission_denied(request)

        return super(OrderLineList, self).get(request, format)
