from django.forms import widgets


class SwitchWidget(widgets.CheckboxInput):
    template_name = 'widgets/switch.html'
