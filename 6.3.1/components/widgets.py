import json
import numbers
import uuid

from django import forms
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils import formats

try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_str as force_text

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from simplepro.components import utils


class Input:
    needs_multipart_form = False
    is_hidden = False
    attrs = {}
    is_required = False

    def get_context(self, name, value, attrs):
        context = {}
        context['widget'] = {
            'name': name,
            'is_hidden': self.is_hidden,
            'required': self.is_required,
            'value': self.format_value(value),
            'attrs': self.build_attrs(self.attrs, attrs),
            'template_name': self.template_name,
        }
        return context

    def format_value(self, value):
        """
        返回在模板中呈现时应该出现的值。
        """
        if value == '' or value is None:
            return None
        if self.is_localized:
            return formats.localize_input(value)
        return str(value)

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of item and this widget's name, return the value
        of this widget or None if it's not provided.
        """
        return data.get(name)

    def id_for_label(self, id_):
        """
        给定字段的ID，返回此小部件的HTML ID属性，以供<label>使用。
        如果没有可用的ID，则返回None。
        这个钩子是必需的，因为一些小部件有多个HTML元素，因此有多个id。
        在这种情况下，这个方法应该返回一个ID值，该值对应于小部件标记中的第一个ID。
        """
        return id_

    def use_required_attribute(self, initial):
        return not self.is_hidden

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build an attribute dictionary."""
        return {**base_attrs, **(extra_attrs or {})}

    def value_omitted_from_data(self, data, files, name):
        return name not in data

    def get_bind_attr(self, attrs=None):
        """
        获取该控件需要绑定的变量参数
        :return:
        """
        if not attrs:
            self.bind_attr = {}
            return
        for key, value in attrs.items():
            if key[0] == ":":
                if isinstance(value, str):
                    self.bind_attr[value] = ''
                elif isinstance(value, dict):
                    for a, b in value.items():
                        self.bind_attr[a] = b
                else:
                    continue


class RadioInput(forms.IntegerField, Input):
    class Media:
        pass

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super(RadioInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/radio.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'choices': self.choices
        }))


class CheckboxInput(forms.ChoiceField, Input):
    class Media:
        pass

    def __init__(self, items, *args, **kwargs):
        super(CheckboxInput, self).__init__(*args, **kwargs)
        self.choices = items

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/checkbox.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'choices': json.dumps(self.choices)
        }))


class SwitchInput(forms.BooleanField, Input):
    class Media:
        pass

    def __init__(self, *args, **kwargs):
        super(SwitchInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/switch.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
        }))


class InputNumberInput(forms.IntegerField, Input):
    class Media:
        pass

    def __init__(self, max_value, min_value, *args, **kwargs):
        super(InputNumberInput, self).__init__(*args, **kwargs)
        self.max_value = max_value
        self.min_value = min_value

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/input_number.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'max_value': self.max_value,
            'min_value': self.min_value
        }))


class SliderInput(forms.IntegerField, Input):
    class Media:
        pass

    def __init__(self, min_value=None, max_value=None, input_size=None, step=None, show_tooltip=True, vertical=False,
                 height='100px', width='200px', show_input=False, *args, **kwargs):
        super(SliderInput, self).__init__(*args, **kwargs)

        self.max_value = max_value
        self.min_value = min_value
        self.input_size = input_size
        self.step = step
        self.show_tooltip = show_tooltip
        self.vertical = vertical
        self.height = height
        self.width = width
        self.show_input = show_input

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/slider.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'max_value': self.max_value,
            'min_value': self.min_value,
            'input_size': self.input_size,
            'step': self.step,
            'show_tooltip': self.show_tooltip,
            'vertical': self.vertical,
            'height': self.height,
            'width': self.width,
            'show_input': self.show_input
        }))


class ImageInput(forms.CharField, Input):
    class Media:
        pass

    def __init__(self, action=None, drag=False, accept=None, *args, **kwargs):
        super(ImageInput, self).__init__(*args, **kwargs)
        self.action = action
        self.drag = drag
        self.accept = accept

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/image.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'action': self.action,
            'drag': self.drag,
            'accept': self.accept
        }))


class RateInput(forms.FloatField, Input):
    class Media:
        pass

    def __init__(self, max_value=5, allow_half=False, disabled=False, show_score=True, *args, **kwargs):
        super(RateInput, self).__init__(*args, **kwargs)
        self.max_value = max_value
        self.allow_half = allow_half
        self.disabled = disabled
        self.show_score = show_score

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/rate.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'max_value': self.max_value,
            'allow_half': self.allow_half,
            'disabled': self.disabled,
            'show_score': self.show_score
        }))


class TimeInput(forms.TimeField, Input):
    supports_microseconds = True
    template_name = 'admin/components/time.html'

    class Media:
        pass

    def __init__(self, verbose_name=None, options={}, prefix_icon='el-icon-date', clear_icon='el-icon-circle-close',
                 align='left',
                 size=None, clearable=True, editable=True, disabled=False, readonly=False, *args, **kwargs):
        super(TimeInput, self).__init__(*args, **kwargs)
        self.verbose_name = verbose_name

        self.options = options
        self.prefix_icon = prefix_icon
        self.clear_icon = clear_icon
        self.align = align
        self.size = size
        self.clearable = clearable
        self.editable = editable
        self.disabled = disabled
        self.readonly = readonly

    def build_attrs(self):
        options = self.options
        if options:

            if not isinstance(options, str):
                if isinstance(options, dict):
                    options = json.dumps(options)
        attrs = ''

        
        attrs += '\tprefix_icon=\'{}\''.format(self.prefix_icon)
        attrs += '\tclear_icon=\'{}\''.format(self.clear_icon)
        attrs += '\talign=\'{}\''.format(self.align)
        attrs += '\tsize=\'{}\''.format(self.size)
        attrs += '\t:clearable={}'.format(str(self.clearable).lower())
        attrs += '\t:editable={}'.format(str(self.editable).lower())
        attrs += '\t:disabled={}'.format(str(self.disabled).lower())
        attrs += '\t:readonly={}'.format(str(self.readonly).lower())

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string(self.template_name, {
            'value': value,
            'name': trim_name(name),
            'raw_name': name,
            'verbose_name': self.verbose_name,
            'attrs': self.build_attrs(),
            'picker_options': self.options
        }))


class DateInput(forms.DateField, TimeInput):
    template_name = 'admin/components/date.html'

    def __init__(self, *args, **kwargs):
        super(DateInput, self).__init__(*args, **kwargs)


class DateTimeInput(forms.DateField, TimeInput):
    template_name = 'admin/components/datetime.html'

    def __init__(self, *args, **kwargs):
        super(DateTimeInput, self).__init__(*args, **kwargs)


class CharInput(forms.CharField, Input):
    """
    文本输入框
    """

    class Media:
        pass

    def __init__(self, input_type='text', placeholder=None, clearable=True, show_password=False,
                 min_length=None, disabled=False, size=None, prefix_icon=None, suffix_icon=None, rows=None,
                 autocomplete=None,
                 readonly=None, max_value=None, min_value=None, step=None, resize=None, autofocus=False,
                 show_word_limit=False, slot=None, slot_text='', style=None, *args, **kwargs):
        super(CharInput, self).__init__(*args)
        self.items = {
            'type': input_type,
            'placeholder': placeholder,
            ':clearable': clearable,
            ':show-password': show_password,
            'disabled': disabled,
            'size': size,
            'prefix-icon': prefix_icon,
            'suffix-icon': suffix_icon,
            'rows': rows,
            'autocomplete': autocomplete,
            'readonly': readonly,
            'maxlength': kwargs.get('max_length'),
            'minlength': min_length,
            'max': max_value,
            'min': min_value,
            'step': step,
            'resize': resize,
            'autofocus': autofocus,
            ':show-word-limit': show_word_limit,
            
        }
        self.slot = slot
        self.slot_text = slot_text
        self.style = style

    def build_attrs(self):
        attrs = ""
        for f in self.items:
            val = self.items.get(f)
            if f == 'disabled' and not val:
                continue
            if val is not None:
                if isinstance(val, bool):
                    val = str(val).lower()
                attrs += '\t{}=\"{}\"'.format(f, val)

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        raw_name = name
        name = trim_name(name)

        return mark_safe(render_to_string('admin/components/char.html', {
            'value': conditional_escape(force_text(value)),
            'name': name,
            'raw_name': raw_name,
            'attrs': self.build_attrs(),
            'slot': self.slot,
            'slot_text': self.slot_text,
            'style': self.style
        }))



def trim_name(name):
    return name.replace('-', '_')
















class SelectInput(forms.Widget, Input):
    choices = ()
    template_name = 'admin/components/select.html'
    multi_select = False

    def __init__(self, name=None, value=None, options=[], verbose_name=None, action=None, attrs={}, *args, **kwargs):
        super(SelectInput, self).__init__(*args, **kwargs)
        self.name = name
        self.value = value
        self.verbose_name = verbose_name
        self.options = options
        self.action = action
        self.attrs = attrs

    def render(self, *args, **kwargs):

        if len(args) == 3:
            self.name = args[0]
            self.value = args[1]
        elif len(args) == 0:
            self.value = kwargs.get('value')
        if isinstance(self.value, bool):
            self.value = '{}'.format(str(self.value).lower())
        elif isinstance(self.value, str) or isinstance(self.value, uuid.UUID):
            self.value = '"{}"'.format(self.value)
        if self.value is None:
            self.value = '""'

        if self.action is None:
            self.action = ''

        return mark_safe(render_to_string(self.template_name, {
            'value': self.value,
            'name': trim_name(self.name),
            'raw_name': self.name,
            'verbose_name': self.verbose_name,
            'options': json.dumps(self.options),
            'attrs': utils.get_attrs(self.attrs),
            'action': self.action,
            'multi_select': self.multi_select
        }))


class MultiSelectInput(SelectInput):
    template_name = 'admin/components/select.html'

    allow_multiple_selected = True
    multi_select = True

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

    def value_omitted_from_data(self, data, files, name):
        
        
        return False


class ManyToManyInput(MultiSelectInput):
    template_name = 'admin/components/many_to_many.html'


class TransferInput(MultiSelectInput):
    template_name = 'admin/components/transfer.html'

    def __init__(self, *args, **kwargs):
        super(TransferInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []

        
        is_number = False
        if self.options:
            for i in self.options:
                if isinstance(i.get("id"), numbers.Number):
                    is_number = True
                    break
        if not is_number:
            value = [str(item) for item in value]

        return mark_safe(render_to_string(self.template_name, {
            'value': value,
            'name': trim_name(name),
            'raw_name': name,
            'verbose_name': self.verbose_name,
            'options': json.dumps(self.options),
            'attrs': utils.get_attrs(self.attrs),
            'action': self.action
        }))


class AMapInput(forms.CharField, Input):
    class Media:
        js = ('https://webapi.amap.com/maps?v=1.4.15&key=be7ccd1b33d98e304c173a0d256437d7',)
        pass

    def __init__(self, api_key, width, height, style, pick_type, *args, **kwargs):
        self.attrs = {
            'api_key': api_key,
            'width': width,
            'height': height,
            'style': style,
            'pick_type': pick_type
        }
        super(AMapInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/amap.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'attrs': self.attrs
        }))


class VideoInput(forms.CharField, Input):

    def __init__(self, *args, **kwargs):
        super(VideoInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/video.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'attrs': self.attrs
        }))


class TreeComboboxInput(forms.Widget, Input):
    choices = ()
    field_name = None

    def __init__(self, *args, strictly=False, queryset, **kwargs):
        self.queryset_fn = queryset
        self.strictly = strictly

        super(TreeComboboxInput, self).__init__(*args, **kwargs)

    def _get_tree_data(self, qs):
        

        _filter = {
            f'{self.field_name}__isnull': True
        }

        _new_qs = qs.filter(**_filter)
        options = []

        for item in _new_qs:
            _result = self._get_item(item)

            children = self._get_children(qs, item)
            if children:
                _result['children'] = children
            options.append(_result)
        return options

    def _get_children(self, qs, parent):
        
        _filter = {
            f'{self.field_name}': parent
        }
        _list = qs.filter(**_filter)
        ds = []
        if _list.count() > 0:
            for item in _list:
                _result = self._get_item(item)
                _temp = self._get_children(qs, item)
                if _temp:
                    _result['children'] = _temp
                ds.append(_result)
        return ds

    def _get_item(self, item):
        return {
            'value': item.id,
            'label': str(item),
        }

    def render(self, name, value, attrs=None, renderer=None):
        self.field_name = name

        qs = self.choices.queryset

        options = []
        if self.queryset_fn:
            
            if callable(self.queryset_fn):
                qs = self.queryset_fn(qs)
            elif isinstance(self.queryset_fn, QuerySet):
                qs = self.queryset_fn

            
            if not isinstance(qs, QuerySet):
                raise ValueError('queryset must be a QuerySet or a function')
            
            options = self._get_tree_data(qs)

        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/tree_combobox.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'attrs': self.attrs,
            'options': json.dumps(options),
            'strictly': self.strictly
        }))
