from .order.urls import urlpatterns as orderurls
from .catalogue.urls import urlpatterns as catalogueurls


from oscarapi.app import RESTApiApplication

from rest_framework.urlpatterns import format_suffix_patterns


class MyRESTApiApplication(RESTApiApplication):

    def get_urls(self):
        urls = orderurls.urls + catalogueurls.urls

        return format_suffix_patterns(urls) + super(MyRESTApiApplication, self).get_urls() + catalogueurls.dynamic_urls


application = MyRESTApiApplication()
