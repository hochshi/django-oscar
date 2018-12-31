from django.conf import settings
from oscar.core.loading import get_model

from rest_framework import generics

from .serializers import OrderLineAttributeSerializer, OrderLineSerializer
from rest_framework import viewsets
from dynamic_rest.viewsets import WithDynamicViewSetMixin, DynamicModelViewSet

from oscarapi.serializers import (
    CheckoutSerializer,
    OrderSerializer, UserAddressSerializer
)
from oscarapi.signals import oscarapi_post_checkout
from oscarapi.views.utils import parse_basket_from_hyperlink

from .serializers import OrderSerializer
from ..permissions import IsOwnerOrStaff

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


class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrStaff, )

    def get_queryset(self):
        qs = Order.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)


class PendingOrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrStaff, )

    def get_queryset(self):
        qs = Order.objects.all()
        return qs.filter(status=settings.OSCAR_INITIAL_ORDER_STATUS)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrStaff,)

