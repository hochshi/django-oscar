from django.conf.urls import url
from .views import *
from ..utils import URLHolder


urls = [
    url(r'^orderlineattributes/(?P<pk>[0-9]+)/$', OrderLineAttributeDetail.as_view(),
        name='order-lineattributes-detail'),
    url(r'^orderlines/(?P<pk>[0-9]+)/$', OrderLineDetail.as_view(), name='order-lines-detail'),
    url(r'^orders/(?P<pk>[0-9]+)/lines/$', OrderLineList.as_view(), name='order-lines-list'),
    url(r'^pendingorders/$', PendingOrderList.as_view(), name='order-list'),
    url(r'^orders/$', OrderList.as_view(), name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$', OrderDetail.as_view(), name='order-detail'),
]

dynamic_urls = [

]

urlpatterns = URLHolder(urls=urls, dynamic_urls=dynamic_urls)
