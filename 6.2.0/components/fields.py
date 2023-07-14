import uuid
from inspect import isfunction

from django import forms
from django.core import exceptions
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from simplepro.components.widgets import *
from simplepro.components import utils


class RadioFormField(forms.fields.IntegerField):
    """ custom form field """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': RadioInput()
        })
        super(RadioFormField, self).__init__(*args, **kwargs)


class RadioField(models.IntegerField):
    """ custom model field """

    def __init__(self, *args, **kwargs):
        super(RadioField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': RadioFormField,
        }
        defaults.update(kwargs)
        r = super(RadioField, self).formfield(**defaults)

        r.widget = RadioInput(choices=self.choices)
        return r


class CheckboxFormField(forms.fields.CharField):
    """ custom form field """

    def __init__(self, choices, *args, **kwargs):
        kwargs.update({
            'widget': CheckboxInput(choices)
        })
        super(CheckboxFormField, self).__init__(*args, **kwargs)


class CheckboxField(models.CharField):
    """ custom model field """

    def __init__(self, choices=None, *args, **kwargs):
        
        self.items = choices
        super(CheckboxField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CheckboxFormField,
            'choices': self.items
        }
        defaults.update(kwargs)
        r = super(CheckboxField, self).formfield(**defaults)
        r.widget = CheckboxInput(items=self.items)
        return r


class SwitchFormField(forms.fields.BooleanField):
    """ custom form field """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': SwitchInput()
        })
        super(SwitchFormField, self).__init__(*args, **kwargs)


class SwitchField(models.BooleanField):
    """ custom model field """

    def __init__(self, *args, **kwargs):
        super(SwitchField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': SwitchFormField,
        }
        defaults.update(kwargs)
        r = super(SwitchField, self).formfield(**defaults)
        return r


class InputNumberFormField(forms.fields.IntegerField):
    """ custom form field """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': InputNumberInput(max_value=kwargs.get('max_value'), min_value=kwargs.get('min_value'))
        })
        super(InputNumberFormField, self).__init__(*args, **kwargs)


class InputNumberField(models.IntegerField):
    """
     InputNumberField
     document: https://simpleui.72wo.com/docs/simplepro/components.html
    """
    max_value = None
    min_value = None

    def __init__(self, *args, **kwargs):
        if 'max_value' in kwargs:
            max_value = kwargs.pop('max_value')
            self.max_value = max_value
        if 'min_value' in kwargs:
            min_value = kwargs.pop('min_value')
            self.min_value = min_value
        super(InputNumberField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': InputNumberFormField,
            'min_value': self.min_value,
            'max_value': self.max_value
        }
        defaults.update(kwargs)
        r = super(InputNumberField, self).formfield(**defaults)

        r.widget = InputNumberInput(max_value=self.max_value, min_value=self.min_value)
        return r


class SliderField(models.IntegerField):
    params = ['min_value', 'max_value', 'input_size', 'step', 'show_tooltip', 'vertical', 'height', 'width',
              'show_input']

    def __init__(self, *args, **kwargs):
        

        items = {}
        for item in self.params:
            if item in kwargs:
                items[item] = kwargs.pop(item)
        self.items = items
        self.__dict__.update(items)
        super(SliderField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': InputNumberFormField,
        }
        defaults.update(kwargs)
        r = super(SliderField, self).formfield(**defaults)

        r.widget = SliderInput(**self.items)
        return r


class ImageFormField(forms.fields.CharField):
    """ custom form field """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': ImageInput(action=kwargs.pop('action'), drag=kwargs.pop('drag'), accept=kwargs.pop('accept'))
        })
        super(ImageFormField, self).__init__(*args, **kwargs)


class ImageField(models.CharField):

    def __init__(self, drag=False, action=None,
                 accept=".png,.jpg,.jpeg,.gif,.bmp,.webp,.psd,.icns,.icon,.heic,.heif,.tiff,.tif",
                 *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 256  
        super(ImageField, self).__init__(*args, **kwargs)
        self.action = action
        self.drag = drag
        self.accept = accept

    def formfield(self, **kwargs):
        defaults = {
            'form_class': ImageFormField,
            'action': self.action,
            'drag': self.drag,
            'accept': self.accept
        }
        defaults.update(kwargs)
        r = super(ImageField, self).formfield(**defaults)

        return r


class RateField(models.FloatField):

    def __init__(self, max_value=5, allow_half=False, disabled=False, show_score=True, *args, **kwargs):
        
        self.max_value = max_value
        self.allow_half = allow_half
        self.disabled = disabled
        self.show_score = show_score

        super(RateField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        r = super(RateField, self).formfield()
        r.widget = RateInput(self.max_value, self.allow_half, self.disabled, self.show_score)
        return r


class TimeField(models.TimeField):

    def __init__(self, options={}, prefix_icon='el-icon-date', clear_icon='el-icon-circle-close', align='left',
                 size=None, clearable=True, editable=True, disabled=False, readonly=False,
                 *args,
                 **kwargs):
        super(TimeField, self).__init__(*args, **kwargs)

        self.items = {
            'options': options,
            'prefix_icon': prefix_icon,
            'clear_icon': clear_icon,
            'align': align,
            'size': size,
            'clearable': clearable,
            'editable': editable,
            'disabled': disabled,
            'readonly': readonly
        }

        if 'verbose_name' in kwargs:
            self.items['verbose_name'] = kwargs.get('verbose_name')

    def formfield(self, **kwargs):
        r = super(TimeField, self).formfield()
        r.widget = TimeInput(**self.items)
        return r


class DateField(models.DateField):

    def __init__(self, options={}, prefix_icon='el-icon-date', clear_icon='el-icon-circle-close', align='left',
                 size=None, clearable=True, editable=True, disabled=False, readonly=False,
                 *args,
                 **kwargs):
        if 'verbose_name' in kwargs:
            self.verbose_name = kwargs.get('verbose_name')
        super(DateField, self).__init__(*args, **kwargs)
        self.items = {
            'options': options,
            'prefix_icon': prefix_icon,
            'clear_icon': clear_icon,
            'align': align,
            'size': size,
            'clearable': clearable,
            'editable': editable,
            'disabled': disabled,
            'readonly': readonly
        }

        if 'verbose_name' in kwargs:
            self.items['verbose_name'] = kwargs.get('verbose_name')

    def formfield(self, **kwargs):
        r = super(DateField, self).formfield()
        r.widget = DateInput(**self.items)
        return r


class DateTimeField(models.DateTimeField):

    def __init__(self, options={}, prefix_icon='el-icon-date', clear_icon='el-icon-circle-close', align='left',
                 size=None, clearable=True, editable=True, disabled=False, readonly=False,
                 *args,
                 **kwargs):
        if 'verbose_name' in kwargs:
            self.verbose_name = kwargs.get('verbose_name')
        super(DateTimeField, self).__init__(*args, **kwargs)
        self.items = {
            'options': options,
            'prefix_icon': prefix_icon,
            'clear_icon': clear_icon,
            'align': align,
            'size': size,
            'clearable': clearable,
            'editable': editable,
            'disabled': disabled,
            'readonly': readonly
        }

        if 'verbose_name' in kwargs:
            self.items['verbose_name'] = kwargs.get('verbose_name')

    def formfield(self, **kwargs):
        r = super(DateTimeField, self).formfield()
        r.widget = DateTimeInput(**self.items)
        return r


class CharFormField(forms.fields.CharField):
    fields = ['input_type', 'max_length', 'min_length'
        , 'placeholder', 'clearable', 'show_password', 'disabled', 'size',
              'prefix_icon', 'suffix_icon', 'rows', 'autocomplete', 'readonly',
              'max_value', 'min_value', 'step', 'resize', 'autofocus', 'show_word_limit', 'slot', 'slot_text', 'style']

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': CharInput(**kwargs)
        })
        for f in self.fields:
            if f in kwargs:
                kwargs.pop(f)
        super(CharFormField, self).__init__(*args, **kwargs)


class CharField(models.CharField):

    def __init__(self, input_type='text', placeholder=None, clearable=True, show_password=False,
                 min_length=None, disabled=False, size=None, prefix_icon=None, suffix_icon=None, rows=None,
                 autocomplete=None,
                 readonly=None, max_value=None, min_value=None, step=None, resize=None, autofocus=False,
                 show_word_limit=False,
                 slot=None, slot_text='', style=None,
                 *args, **kwargs):
        self.items = {
            'input_type': input_type,
            'max_length': kwargs.get('max_length'),
            'min_length': min_length,
            'placeholder': placeholder,
            'clearable': clearable,
            'show_password': show_password,
            'disabled': disabled,
            'size': size,
            'prefix_icon': prefix_icon,
            'suffix_icon': suffix_icon,
            'rows': rows,
            'autocomplete': autocomplete,
            'readonly': readonly,
            'max_value': max_value,
            'min_value': min_value,
            'step': step,
            'resize': resize,
            'autofocus': autofocus,
            'show_word_limit': show_word_limit,
            'slot': slot,
            'slot_text': slot_text,
            'style': style
        }

        super(CharField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CharFormField,
        }

        defaults.update(kwargs)
        defaults.update(self.items)

        r = super(CharField, self).formfield(**defaults)
        return r


class AMapFormField(forms.fields.CharField):
    """ custom form field """

    def __init__(self, *args, **kwargs):
        fields = ['api_key', 'width', 'height', 'style', 'pick_type']

        kwargs.update({
            'widget': AMapInput(*args, **kwargs)
        })

        for f in fields:
            kwargs.pop(f)

        super(AMapFormField, self).__init__(*args, **kwargs)


class AMapField(models.CharField):
    """ custom model field """

    def __init__(self, api_key='be7ccd1b33d98e304c173a0d256437d7',
                 width='500px',
                 height="300px",
                 style='',
                 pick_type='geo',  
                 *args,
                 **kwargs):
        self.params = {
            'api_key': api_key,
            'width': width,
            'height': height,
            'style': style,
            'pick_type': pick_type
        }

        super(AMapField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': AMapFormField
        }
        defaults.update(kwargs)
        defaults.update(self.params)
        r = super(AMapField, self).formfield(**defaults)
        r.widget = AMapInput(**self.params)
        return r


def get_id_value(id):
    if not id:
        return id
    if isinstance(id, numbers.Number):
        return id
    else:
        return str(id)


class ForeignKey(models.ForeignKey):
    """
    OneToMany
    """

    def __init__(self, *args, disabled=None,
                 size=None,
                 clearable=True,
                 placeholder=None,
                 filterable=True,
                 queryset=None,  
                 action=None,  
                 limit=None,
                 **kwargs):
        self.action = action
        self.queryset = queryset
        self.size = size
        self.clearable = clearable
        self.placeholder = placeholder
        self.disabled = disabled
        self.filterable = filterable
        self.limit = limit

        super(ForeignKey, self).__init__(*args, **kwargs)

    def get_attrs(self):
        if not self.placeholder:
            self.placeholder = self.verbose_name
        attrs = {
            'size': self.size,
            'placeholder': self.placeholder,
        }
        if self.disabled:
            attrs['disabled'] = ''
        if self.clearable:
            attrs['clearable'] = ''
        if self.filterable:
            attrs['filterable'] = ''
        return attrs

    def formfield(self, *, using=None, **kwargs):
        if isinstance(self.remote_field.model, str):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.remote_field.model))

        defaults = {
            'form_class': forms.ModelChoiceField,
            'queryset': self.remote_field.model._default_manager.using(using),
            'to_field_name': self.remote_field.field_name,
            **kwargs,
            
        }
        r = super().formfield(**defaults)
        

        widget = r.widget
        options = []
        
        qs = widget.choices.queryset.all()
        if self.queryset:
            if isfunction(self.queryset):
                qs = self.queryset()
            else:
                qs = self.queryset

        if self.limit:
            qs = qs[:self.limit]
        datas = list(qs)
        for item in datas:
            options.append({
                'id': get_id_value(item.pk),
                'text': str(item)
            })
        action = self.action

        if action is None:
            if hasattr(r.widget, 'get_url'):
                action = r.widget.get_url()
        r.widget = SelectInput(verbose_name=self.verbose_name, name=self.name, options=options, attrs=self.get_attrs(),
                               action=action)
        return r


class OneToOneField(models.OneToOneField):
    """
    OneToOneField
    """

    def __init__(self, *args, disabled=None,
                 size=None,
                 clearable=True,
                 placeholder=None,
                 filterable=True,
                 queryset=None,  
                 action=None,  
                 limit=None,
                 **kwargs):
        self.action = action
        self.queryset = queryset
        self.size = size
        self.clearable = clearable
        self.placeholder = placeholder
        self.disabled = disabled
        self.filterable = filterable
        self.limit = limit
        super(OneToOneField, self).__init__(*args, **kwargs)

    def get_attrs(self):
        if self.placeholder is None:
            self.placeholder = self.verbose_name
        attrs = {
            'size': self.size,
            'placeholder': self.placeholder,
        }
        if self.disabled:
            attrs['disabled'] = ''
        if self.clearable:
            attrs['clearable'] = ''
        if self.filterable:
            attrs['filterable'] = ''
        return attrs

    def formfield(self, **kwargs):
        if self.remote_field.parent_link:
            return None
        r = super().formfield(**kwargs)
        widget = r.widget
        options = []
        
        qs = widget.choices.queryset.all()
        if self.queryset:
            if isfunction(self.queryset):
                qs = self.queryset()
            else:
                qs = self.queryset

        if self.limit:
            qs = qs[:self.limit]
        datas = list(qs)

        for item in datas:
            options.append({
                'id': get_id_value(item.pk),
                'text': str(item)
            })
        action = self.action
        if action is None:
            if hasattr(r.widget, 'get_url'):
                action = r.widget.get_url()

        r.widget = SelectInput(verbose_name=self.verbose_name, name=self.name, options=options, attrs=self.get_attrs(),
                               action=action)
        return r


class ManyToManyField(models.ManyToManyField):
    """
    ManyToManyField
    """

    def __init__(self, *args,
                 disabled=None,
                 size=None,
                 clearable=True,
                 placeholder=None,
                 filterable=True,
                 queryset=None,  
                 action=None,  
                 limit=None, **kwargs):
        super(ManyToManyField, self).__init__(*args, **kwargs)

        self.action = action
        self.queryset = queryset
        self.size = size
        self.clearable = clearable
        self.placeholder = placeholder
        self.disabled = disabled
        self.filterable = filterable
        self.limit = limit

    def get_attrs(self):
        if self.placeholder is None:
            self.placeholder = self.verbose_name
        attrs = {
            'size': self.size,
            'placeholder': self.placeholder,
        }
        if self.disabled:
            attrs['disabled'] = ''
        if self.clearable:
            attrs['clearable'] = ''
        if self.filterable:
            attrs['filterable'] = ''
        return attrs

    def formfield(self, *, using=None, **kwargs):
        
        
        qs = self.remote_field.model._default_manager.using(using)
        defaults = {
            'form_class': forms.ModelMultipleChoiceField,
            'queryset': qs,
            **kwargs,
        }
        
        
        if defaults.get('initial') is not None:
            initial = defaults['initial']
            if callable(initial):
                initial = initial()
            defaults['initial'] = [i.pk for i in initial]
        r = super().formfield(**defaults)
        
        options = []
        datas = list(qs)
        for item in datas:
            options.append({
                'id': get_id_value(item.pk),
                'text': str(item)
            })
        action = self.action
        if action is None:
            if hasattr(r.widget, 'get_url'):
                action = r.widget.get_url()

        r.widget = MultiSelectInput(verbose_name=self.verbose_name, name=self.name, options=options,
                                    attrs=self.get_attrs(), action=action)
        return r


class IntegerField(models.IntegerField):
    placeholder = None
    clearable = True

    def __str__(self, *args, size=None,
                clearable=True,
                placeholder=None,
                filterable=True,
                **kwargs):
        self.attrs = {}
        if size is not None:
            self.attrs['size'] = size
        if clearable is not None:
            self.attrs['clearable'] = ''
        if placeholder is not None:
            self.attrs['placeholder'] = placeholder
        if filterable is not None:
            self.attrs['filterable'] = ''

        super(IntegerField, self).__str__(*args, **kwargs)

        self.placeholder = placeholder
        self.clearable = clearable

    def get_attrs(self):
        return self.attrs

    def formfield(self, **kwargs):
        r = super().formfield(**{
            'form_class': forms.IntegerField,
            **kwargs,
        })

        if hasattr(r, 'choices'):
            choices = r.choices
            options = []
            for item in choices:
                options.append({
                    'id': get_id_value(item[0]),
                    'text': str(item[1])
                })

            r.widget = SelectInput(verbose_name=self.verbose_name, name=self.name, options=options,
                                   attrs={})
        else:
            placeholder = self.placeholder
            if not placeholder:
                placeholder = self.verbose_name
            r.widget = CharInput(input_type='number', clearable=self.clearable, placeholder=placeholder)

        return r


class TransferField(models.ManyToManyField):
    """
    基于穿梭框的多对多字段
    """

    def __init__(self, *args,
                 filterable=True,
                 placeholder=None,
                 titles=None,
                 button_texts=None,
                 format=None,
                 queryset=None,
                 limit=None,
                 action=None
                 , **kwargs):
        super(TransferField, self).__init__(*args, **kwargs)
        self.queryset = queryset
        self.limit = limit
        self.action = action

        attrs = {}
        if filterable:
            attrs['filterable'] = ''
        if placeholder:
            attrs['filter-placeholder'] = placeholder
        if titles:
            attrs[':titles'] = titles
        if button_texts:
            attrs[':button-texts'] = button_texts
        if format:
            attrs[':format'] = format
        self.attrs = attrs

    def formfield(self, *, using=None, **kwargs):
        qs = self.remote_field.model._default_manager.using(using)
        defaults = {
            'form_class': forms.ModelMultipleChoiceField,
            'queryset': qs,
            **kwargs,
        }
        
        
        if defaults.get('initial') is not None:
            initial = defaults['initial']
            if callable(initial):
                initial = initial()
            defaults['initial'] = [i.pk for i in initial]
        r = super().formfield(**defaults)
        

        if self.queryset:
            if isfunction(self.queryset):
                qs = self.queryset()
            else:
                qs = self.queryset

        if self.limit:
            qs = qs[:self.limit]

        options = []
        datas = list(qs)
        for item in datas:
            options.append({
                'id': get_id_value(item.pk),
                'text': str(item)
            })
        action = self.action

        if action is None:
            if hasattr(r.widget, 'get_url'):
                action = r.widget.get_url()

        r.widget = TransferInput(verbose_name=self.verbose_name, name=self.name, options=options, attrs=self.attrs,
                                 action=action)
        return r


class VideoFormField(forms.fields.CharField):
    """ video form field """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': VideoInput()
        })
        super(VideoFormField, self).__init__(*args, **kwargs)


class VideoField(models.CharField):
    """ video model field """

    def __init__(self, *args, **kwargs):
        super(VideoField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': VideoFormField,
        }
        defaults.update(kwargs)
        r = super(VideoField, self).formfield(**defaults)
        r.widget = VideoInput()
        return r


class TreeComboboxFormField(forms.ModelChoiceField):
    """ tree combobox form field """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': TreeComboboxInput()
        })
        super(TreeComboboxFormField, self).__init__(*args, **kwargs)


class TreeComboboxField(models.ForeignKey):
    """ tree combobox field """

    def __init__(self, *args, strictly=False, queryset=None, **kwargs, ):
        self.queryset_fn = queryset
        self.strictly = strictly
        super(TreeComboboxField, self).__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        
        
        
        
        
        
        
        
        
        
        
        pass

    def formfield(self, **kwargs):
        
        
        defaults = {
            
        }
        defaults.update(kwargs)
        r = super(TreeComboboxField, self).formfield(**defaults)
        r.widget = TreeComboboxInput(queryset=self.queryset_fn, strictly=self.strictly)
        return r
