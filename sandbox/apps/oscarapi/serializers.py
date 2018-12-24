from oscar.core.loading import get_model
from oscarapi.serializers import OrderLineSerializer as OLS
from oscarapi.serializers import OrderLineAttributeSerializer as OLAS
from rest_framework import exceptions, serializers

Order = get_model('order', 'Order')
OrderLine = get_model('order', 'Line')
OrderLineAttribute = get_model('order', 'LineAttribute')
Option = get_model('catalogue', 'Option')


class OrderLineValueField(serializers.RelatedField):

    def to_representation(self, value):
        if value.option.is_file:
            return serializers.FileField(source=value.value).to_representation(value.value)
        return str(value.value)


class OrderLineAttributeSerializer(OLAS):

    value = OrderLineValueField(source='*', read_only=True)

    class Meta:
        model = OrderLineAttribute
        fields = '__all__'


class OrderLineSerializer(OLS):
    attributes = OrderLineAttributeSerializer(
        many=True, fields=('url', 'option', 'value', 'type'), required=False)
