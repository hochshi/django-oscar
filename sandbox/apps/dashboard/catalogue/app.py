from django.conf.urls import url

from oscar.apps.dashboard.catalogue.app import CatalogueApplication
from oscar.core.loading import get_class


class CustomCatalogueApplication(CatalogueApplication):
    option_list_view = get_class('dashboard.catalogue.views', 'OptionListView')
    option_create_view = get_class('dashboard.catalogue.views', 'OptionCreateView')
    option_update_view = get_class('dashboard.catalogue.views', 'OptionUpdateView')
    option_delete_view = get_class('dashboard.catalogue.views', 'OptionDeleteView')

    def get_urls(self):
        urls = super().get_urls()
        option_urls = [
            url(r'^option/$',
                self.option_list_view.as_view(),
                name='catalogue-option-list'),
            url(r'^option/create/$',
                self.option_create_view.as_view(),
                name='catalogue-option-create'),
            url(r'^option/(?P<pk>\w+)/update/$',
                self.option_update_view.as_view(),
                name='catalogue-option-update'),
            url(r'^option/(?P<pk>\w+)/delete/$',
                self.option_delete_view.as_view(),
                name='catalogue-option-delete'),
        ]
        return urls + self.post_process_urls(option_urls)



application = CustomCatalogueApplication()
