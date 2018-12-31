from django.conf.urls import url
from django.urls import include
from .views import *
from dynamic_rest.routers import DynamicRouter
from ..utils import URLHolder

router = DynamicRouter()
# router.register('options', DynamicOptionViewSet)
router.register('options', OptionViewSet)

urls = [
    url(r'^options/$', OptionList.as_view(), name='option-list'),
    url(r'^options/(?P<pk>[0-9]+)/$', OptionDetail.as_view(), name='option-detail'),
]

dynamic_urls = [
    url(r'^dynamic/', include(router.urls)),
]

urlpatterns = URLHolder(urls=urls, dynamic_urls=dynamic_urls)
