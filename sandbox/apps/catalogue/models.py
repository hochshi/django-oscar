import logging
import os
from datetime import date, datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.finders import find
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.files.base import File
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Count, Sum
from django.urls import reverse
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language, pgettext_lazy
from treebeard.mp_tree import MP_Node

from oscar.core.loading import get_class, get_classes, get_model
from oscar.core.utils import slugify
from oscar.core.validators import non_python_keyword
from oscar.models.fields import AutoSlugField, NullCharField
from oscar.models.fields.slugfield import SlugField

from oscar.apps.catalogue.abstract_models import AbstractOption


@python_2_unicode_compatible
class Option(AbstractOption):
    # Attribute types
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    RICHTEXT = "richtext"
    DATE = "date"
    DATETIME = "datetime"
    # OPTION = "option"
    # MULTI_OPTION = "multi_option"
    # ENTITY = "entity"
    FILE = "file"
    IMAGE = "image"
    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (RICHTEXT, _("Rich Text")),
        (DATE, _("Date")),
        (DATETIME, _("Datetime")),
        # (OPTION, _("Option")),
        # (MULTI_OPTION, _("Multi Option")),
        # (ENTITY, _("Entity")),
        (FILE, _("File")),
        (IMAGE, _("Image")),
    )
    type = models.CharField(
        choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
        max_length=20, verbose_name=_("Type"))

    REQUIRED, OPTIONAL = ('Required', 'Optional')
    REQUIRED_CHOICES = (
        (REQUIRED, _("Required - a value for this option must be specified")),
        (OPTIONAL, _("Optional - a value for this option can be omitted")),
    )

    required = models.CharField(_("Status"), max_length=128, default=REQUIRED, choices=REQUIRED_CHOICES)

    @property
    def is_required(self):
        return self.required == self.REQUIRED

    # @property
    # def is_option(self):
    #     return self.type == self.OPTION
    #
    # @property
    # def is_multi_option(self):
    #     return self.type == self.MULTI_OPTION

    @property
    def is_file(self):
        return self.type in [self.FILE, self.IMAGE]

    def __str__(self):
        return self.name

    def _save_file(self, value_obj, value):
        # File fields in Django are treated differently, see
        # django.db.models.fields.FileField and method save_form_data
        if value is None:
            # No change
            return
        elif value is False:
            # Delete file
            value_obj.delete()
        else:
            # New uploaded file
            value_obj.value = value
            value_obj.save()

    # def _save_multi_option(self, value_obj, value):
    #     # ManyToMany fields are handled separately
    #     if value is None:
    #         value_obj.delete()
    #         return
    #     try:
    #         count = value.count()
    #     except (AttributeError, TypeError):
    #         count = len(value)
    #     if count == 0:
    #         value_obj.delete()
    #     else:
    #         value_obj.value = value
    #         value_obj.save()

    def _save_value(self, value_obj, value):
        if value is None or value == '':
            value_obj.delete()
            return
        if value != value_obj.value:
            value_obj.value = value
            value_obj.save()

    def save_value(self, product, value):  # noqa: C901 too complex
        ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
        try:
            value_obj = product.attribute_values.get(attribute=self)
        except ProductAttributeValue.DoesNotExist:
            # FileField uses False for announcing deletion of the file
            # not creating a new value
            delete_file = self.is_file and value is False
            if value is None or value == '' or delete_file:
                return
            value_obj = ProductAttributeValue.objects.create(
                product=product, attribute=self)

        if self.is_file:
            self._save_file(value_obj, value)
        elif self.is_multi_option:
            self._save_multi_option(value_obj, value)
        else:
            self._save_value(value_obj, value)

    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' % self.type)
        validator(value)

    # Validators

    def _validate_text(self, value):
        if not isinstance(value, six.string_types):
            raise ValidationError(_("Must be str or unicode"))

    _validate_richtext = _validate_text

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError(_("Must be a float"))

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(_("Must be an integer"))

    def _validate_date(self, value):
        if not (isinstance(value, datetime) or isinstance(value, date)):
            raise ValidationError(_("Must be a date or datetime"))

    def _validate_datetime(self, value):
        if not isinstance(value, datetime):
            raise ValidationError(_("Must be a datetime"))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError(_("Must be a boolean"))

    def _validate_entity(self, value):
        if not isinstance(value, models.Model):
            raise ValidationError(_("Must be a model instance"))

    # def _validate_multi_option(self, value):
    #     try:
    #         values = iter(value)
    #     except TypeError:
    #         raise ValidationError(
    #             _("Must be a list or AttributeOption queryset"))
    #     # Validate each value as if it were an option
    #     # Pass in valid_values so that the DB isn't hit multiple times per iteration
    #     valid_values = self.option_group.options.values_list(
    #         'option', flat=True)
    #     for value in values:
    #         self._validate_option(value, valid_values=valid_values)
    #
    # def _validate_option(self, value, valid_values=None):
    #     if not isinstance(value, get_model('catalogue', 'AttributeOption')):
    #         raise ValidationError(
    #             _("Must be an AttributeOption model object instance"))
    #     if not value.pk:
    #         raise ValidationError(_("AttributeOption has not been saved yet"))
    #     if valid_values is None:
    #         valid_values = self.option_group.options.values_list(
    #             'option', flat=True)
    #     if value.option not in valid_values:
    #         raise ValidationError(
    #             _("%(enum)s is not a valid choice for %(attr)s") %
    #             {'enum': value, 'attr': self})

    def _validate_file(self, value):
        if value and not isinstance(value, File):
            raise ValidationError(_("Must be a file field"))

    _validate_image = _validate_file


@python_2_unicode_compatible
class AbstractOptionValue(models.Model):
    """
    The "through" model for the m2m relationship between catalogue.Product and
    catalogue.ProductAttribute.  This specifies the value of the attribute for
    a particular product

    For example: number_of_pages = 295
    """
    option = models.ForeignKey(
        'catalogue.Option',
        on_delete=models.CASCADE,
        verbose_name=_("Option"))

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True)
    value_boolean = models.NullBooleanField(_('Boolean'), blank=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True)
    value_richtext = models.TextField(_('Richtext'), blank=True, null=True)
    value_date = models.DateField(_('Date'), blank=True, null=True)
    value_datetime = models.DateTimeField(_('DateTime'), blank=True, null=True)
    # value_multi_option = models.ManyToManyField(
    #     'catalogue.AttributeOption', blank=True,
    #     related_name='multi_valued_attribute_values',
    #     verbose_name=_("Value multi option"))
    # value_option = models.ForeignKey(
    #     'catalogue.AttributeOption',
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    #     verbose_name=_("Value option"))
    value_file = models.FileField(
        upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255,
        blank=True, null=True)
    value_image = models.ImageField(
        upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255,
        blank=True, null=True)
    # value_entity = GenericForeignKey(
    #     'entity_content_type', 'entity_object_id')
    #
    # entity_content_type = models.ForeignKey(
    #     ContentType,
    #     blank=True,
    #     editable=False,
    #     on_delete=models.CASCADE,
    #     null=True)
    # entity_object_id = models.PositiveIntegerField(
    #     null=True, blank=True, editable=False)

    def _get_value(self):
        value = getattr(self, 'value_%s' % self.option.type)
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        attr_name = 'value_%s' % self.option.type

        # if self.option.is_option and isinstance(new_value, six.string_types):
        #     # Need to look up instance of AttributeOption
        #     new_value = self.option.option_group.options.get(
        #         option=new_value)
        # elif self.option.is_multi_option:
        #     getattr(self, attr_name).set(new_value)
        #     return

        setattr(self, attr_name, new_value)
        return

    value = property(_get_value, _set_value)

    class Meta:
        abstract = True
        app_label = 'catalogue'
        unique_together = ('attribute', 'product')
        verbose_name = _('Product attribute value')
        verbose_name_plural = _('Product attribute values')

    def __str__(self):
        return self.summary()

    def summary(self):
        """
        Gets a string representation of both the attribute and it's value,
        used e.g in product summaries.
        """
        return u"%s: %s" % (self.option.name, self.value_as_text)

    @property
    def value_as_text(self):
        """
        Returns a string representation of the attribute's value. To customise
        e.g. image attribute values, declare a _image_as_text property and
        return something appropriate.
        """
        property_name = '_%s_as_text' % self.option.type
        return getattr(self, property_name, self.value)

    @property
    def _multi_option_as_text(self):
        return ', '.join(str(option) for option in self.value_multi_option.all())

    @property
    def _richtext_as_text(self):
        return strip_tags(self.value)

    @property
    def _entity_as_text(self):
        """
        Returns the unicode representation of the related model. You likely
        want to customise this (and maybe _entity_as_html) if you use entities.
        """
        return six.text_type(self.value)

    @property
    def value_as_html(self):
        """
        Returns a HTML representation of the attribute's value. To customise
        e.g. image attribute values, declare a _image_as_html property and
        return e.g. an <img> tag.  Defaults to the _as_text representation.
        """
        property_name = '_%s_as_html' % self.option.type
        return getattr(self, property_name, self.value_as_text)

    @property
    def _richtext_as_html(self):
        return mark_safe(self.value)

from oscar.apps.catalogue.models import *  # noqa isort:skip
