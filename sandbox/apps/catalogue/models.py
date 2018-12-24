from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.models.fields import AutoSlugField

from apps.catalogue.abstract_models import OptionTypeMixin, AbstractOptionValue
from oscar.apps.catalogue.abstract_models import AbstractOption

__all__ = []


class Option(OptionTypeMixin):

    name = models.CharField(_("Name"), max_length=128)
    code = AutoSlugField(_("Code"), max_length=128, unique=True,
                         populate_from='name')

    def save_value(self, product, value):  # noqa: C901 too complex
        pass
        # ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
        # try:
        #     value_obj = product.attribute_values.get(attribute=self)
        # except ProductAttributeValue.DoesNotExist:
        #     # FileField uses False for announcing deletion of the file
        #     # not creating a new value
        #     delete_file = self.is_file and value is False
        #     if value is None or value == '' or delete_file:
        #         return
        #     value_obj = ProductAttributeValue.objects.create(
        #         product=product, attribute=self)
        #
        # if self.is_file:
        #     self._save_file(value_obj, value)
        # elif self.is_multi_option:
        #     self._save_multi_option(value_obj, value)
        # else:
        #     self._save_value(value_obj, value)

    class Meta(AbstractOption.Meta):
        abstract = False


class OptionValue(AbstractOptionValue):

    option = models.ForeignKey(
        'catalogue.Option',
        on_delete=models.CASCADE,
        verbose_name=_("Option"))
    product = models.ForeignKey(
        'catalogue.Product',
        on_delete=models.CASCADE,
        related_name='option_values',
        verbose_name=_("Product"))

    class Meta:
        abstract = False
        app_label = 'catalogue'
        verbose_name = _('Product option value')
        verbose_name_plural = _('Product option values')


__all__.append('OptionValue')

from oscar.apps.catalogue.models import *  # noqa isort:skip
