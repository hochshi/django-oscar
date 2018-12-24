from django.conf.urls import url

from oscarapi.app import RESTApiApplication

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


class MyRESTApiApplication(RESTApiApplication):

    def get_urls(self):
        urls = [
            url(r'^orderlineattributes/(?P<pk>[0-9]+)/$', views.OrderLineAttributeDetail.as_view(),
                name='order-lineattributes-detail'),
            url(r'^orderlines/(?P<pk>[0-9]+)/$', views.OrderLineDetail.as_view(), name='order-lines-detail'),
            url(r'^orders/(?P<pk>[0-9]+)/lines/$', views.OrderLineList.as_view(), name='order-lines-list'),
        ]
        # urls = [url(
        #     r'^products/$',
        #     views.ProductList.as_view(), name='product-list')]

        return format_suffix_patterns(urls) + super(MyRESTApiApplication, self).get_urls()


application = MyRESTApiApplication()