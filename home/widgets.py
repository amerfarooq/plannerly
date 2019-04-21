from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

class ColorPickerWidget(forms.Widget):
    
    class Media:
        css = {
            'all': ('css/colorPick.css',)
        }
        js = ('js/colorPick.js',)

    def render(self, name, value, attrs=None, renderer=None):
        output = render_to_string('home/colorpicker.html', {
            'widget_name': name,
        })
        return mark_safe(output)

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)
