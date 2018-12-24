from oscar.apps.basket.abstract_models import AbstractLineAttribute
from django.db import models
from apps.catalogue.abstract_models import AbstractOptionValue


def upload_to(instance, filename):
    return str(instance.line.basket_id) + '/' + filename


class LineAttribute(AbstractOptionValue, AbstractLineAttribute):
    value_file = models.FileField(
        upload_to=upload_to, max_length=255,
        blank=True, null=True)
    value_image = models.ImageField(
        upload_to=upload_to, max_length=255,
        blank=True, null=True)
    value = AbstractOptionValue.value


from oscar.apps.basket.models import *  # noqa isort:skip
