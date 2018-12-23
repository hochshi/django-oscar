from oscar.apps.dashboard.catalogue.views import *
from django.utils.translation import gettext_lazy as _

(AttributeOptionGroupForm, OptionForm) = get_classes('apps.dashboard.catalogue.forms',
                                                     ('AttributeOptionGroupForm', 'OptionForm'))
(OptionTable,) = get_classes('apps.dashboard.catalogue.tables', ('OptionTable',))
Option = get_model('catalogue', 'Option')


class OptionListView(SingleTableView):

    template_name = 'templates/option_list.html'
    model = Option
    table_class = OptionTable
    context_table_name = 'options'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class OptionCreateUpdateView(generic.UpdateView):

    template_name = 'templates/option_form.html'
    model = Option
    form_class = OptionForm

    def forms_invalid(self, *args, **kwargs):
        messages.error(
            self.request,
            _("Your submitted data was not valid - please correct the errors below")
        )
        return super().form_invalid(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = self.get_title()
        return ctx


class OptionCreateView(OptionCreateUpdateView):

    def get_object(self):
        return None

    def get_title(self):
        return _("Add a new Option")

    def get_success_url(self):
        messages.info(self.request, _("Option created successfully"))
        url = reverse("dashboard:catalogue-option-list")
        return url


class OptionUpdateView(OptionCreateUpdateView):

    def get_object(self):
        attribute_option_group = get_object_or_404(Option, pk=self.kwargs['pk'])
        return attribute_option_group

    def get_title(self):
        return _("Update Option '%s'") % self.object.name

    def get_success_url(self):
        messages.info(self.request, _("Option updated successfully"))
        url = reverse("dashboard:catalogue-option-list")
        return url


class OptionDeleteView(generic.DeleteView):

    template_name = 'templates/option_delete.html'
    model = Option

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = _("Delete Option '%s'") % self.object.name

        products = self.object.product_set.count()
        product_classes = self.object.productclass_set.count()
        if any([products, product_classes]):
            ctx['disallow'] = True
            ctx['title'] = _("Unable to delete '%s'") % self.object.name
            if products:
                messages.error(
                    self.request,
                    _("%i products are still assigned to this option") % products
                )
            if product_classes:
                messages.error(
                    self.request,
                    _("%i product classes are still assigned to this option") % product_classes
                )

        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Option deleted successfully"))
        url = reverse("dashboard:catalogue-option-list")
        return url
