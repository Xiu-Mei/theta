from django import forms
from printers.models import Printer


class PrinterForm(forms.ModelForm):
    manufacturer = forms.ChoiceField(label='label', widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'name',
            'class': 'form-control',
            'placeholder': 'LaserJet 2014',

        }
    ))

    class Meta:
        model = Printer
        fields = ['manufacturer', 'name', 'image', 'usb', 'ethernet', 'wireless', 'duplex', 'color', 'type', 'comment']
