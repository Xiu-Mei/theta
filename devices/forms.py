from django import forms
from devices.models import Manufacturer


class ManufacturerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'name',
            'class': 'form-control',
            'placeholder': 'HP',

        }
    ))
    image = forms.FileField(required=False,
                            label='Company Logo',
                            widget=forms.FileInput(
                                attrs={
                                    'accept': "image/*",
                                }))

    class Meta:
        model = Manufacturer
        fields = ['name', 'image']
