from oscar.apps.dashboard.catalogue.forms import *

Option = get_model('catalogue', 'Option')


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['name', 'type', 'required']
