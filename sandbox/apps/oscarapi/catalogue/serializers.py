from oscar.core.loading import get_model
from oscarapi.utils import (
    overridable,
    OscarHyperlinkedModelSerializer
)
from dynamic_rest.serializers import DynamicModelSerializer

from dynamic_rest.serializers import WithDynamicModelSerializerMixin
from rest_framework import exceptions, serializers, generics

Option = get_model('catalogue', 'Option')


class OptionSerializer(OscarHyperlinkedModelSerializer):
    class Meta:
        model = Option
        fields = overridable('OSCARAPI_OPTION_FIELDS', default=(
            'url', 'id', 'name', 'code', 'type', 'status'
        ))


class WithOptionSerializer(WithDynamicModelSerializerMixin, OscarHyperlinkedModelSerializer):
    class Meta:
        model = Option
        fields = overridable('OSCARAPI_OPTION_FIELDS', default=(
            'url', 'id', 'name', 'code', 'type', 'status'
        ))
        name = 'option'


class DynamicOptionSerializer(DynamicModelSerializer):
    class Meta:
        model = Option
        name = 'option'
        fields = overridable('OSCARAPI_OPTION_FIELDS', default=(
            'id', 'name', 'code', 'type', 'status'
        ))
