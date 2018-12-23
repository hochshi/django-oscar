from oscar.apps.dashboard.catalogue.tables import *
from django.utils.translation import ugettext_lazy as _

Option = get_model('catalogue', 'Option')


class OptionTable(DashboardTable):
    name = TemplateColumn(
        verbose_name=_('Name'),
        template_name='templates/option_row_name.html',
        order_by='name')
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='templates/option_row_actions.html',
        orderable=False)

    icon = "reorder"
    caption = ungettext_lazy("%s Option", "%s Options")

    class Meta(DashboardTable.Meta):
        model = Option
        fields = ('name', 'type')
        sequence = ('name', 'type', 'actions')
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
