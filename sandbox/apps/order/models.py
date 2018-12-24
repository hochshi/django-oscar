from oscar.apps.order.abstract_models import AbstractLineAttribute
from apps.catalogue.abstract_models import AbstractOptionValue


class LineAttribute(AbstractLineAttribute, AbstractOptionValue):
    value = AbstractOptionValue.value

from oscar.apps.order.models import *  # noqa isort:skip
