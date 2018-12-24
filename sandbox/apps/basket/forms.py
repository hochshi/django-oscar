from django import forms
from oscar.apps.basket import forms as base_forms
from apps.dashboard.catalogue.forms import ProductForm


class AddToBasketForm(base_forms.AddToBasketForm):

    def _create_product_fields(self, product):
        for option in product.options:
            field = self.get_option_field(option)
            if field:
                self.fields['%s' % option.code] = field

    def get_option_field(self, option):
        """
        Gets the correct form field for a given attribute type.
        """
        return ProductForm.FIELD_FACTORIES[option.type](option)


class SimpleAddToBasketForm(AddToBasketForm):

    def __init__(self, *args, **kwargs):
        super(SimpleAddToBasketForm, self).__init__(*args, **kwargs)
        if 'quantity' in self.fields:
            self.fields['quantity'].initial = 1
            self.fields['quantity'].widget = forms.HiddenInput()

