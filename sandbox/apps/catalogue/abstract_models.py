from abc import abstractmethod
from datetime import date, datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db import models
from django.utils import six
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class OptionTypeMixin(models.Model):

    # Attribute types
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    RICHTEXT = "richtext"
    DATE = "date"
    DATETIME = "datetime"
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

    status = models.CharField(_("Status"), max_length=128, default=REQUIRED, choices=REQUIRED_CHOICES)

    @property
    def is_required(self):
        return self.required == self.REQUIRED

    @property
    def required(self):
        return self.status == self.REQUIRED

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

    def _save_value(self, value_obj, value):
        if value is None or value == '':
            value_obj.delete()
            return
        if value != value_obj.value:
            value_obj.value = value
            value_obj.save()

    @abstractmethod
    def save_value(self, product, value):  # noqa: C901 too complex
        pass
        # Left for reference
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

    def _validate_file(self, value):
        if value and not isinstance(value, File):
            raise ValidationError(_("Must be a file field"))

    _validate_image = _validate_file

    class Meta:
        abstract = True


class AbstractOptionValue(models.Model):

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True)
    value_boolean = models.NullBooleanField(_('Boolean'), blank=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True)
    value_richtext = models.TextField(_('Richtext'), blank=True, null=True)
    value_date = models.DateField(_('Date'), blank=True, null=True)
    value_datetime = models.DateTimeField(_('DateTime'), blank=True, null=True)
    value_file = models.FileField(
        upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255,
        blank=True, null=True)
    value_image = models.ImageField(
        upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255,
        blank=True, null=True)

    def _get_value(self):
        value = getattr(self, 'value_%s' % self.option.type)
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        attr_name = 'value_%s' % self.option.type
        setattr(self, attr_name, new_value)
        return

    value = property(_get_value, _set_value)

    class Meta:
        abstract = True

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

