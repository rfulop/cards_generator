import json

from django import forms
from django.forms import formset_factory, BaseFormSet
from django.urls import reverse

from .constants import DEFAULT_SLOT_IMAGE_SIZE, DEFAULT_MAX_SLOT_IMAGE_SIZE
from .models import CardOutline, CardSlot


class CardOutlineSelectionForm(forms.Form):
    outline = forms.ModelChoiceField(queryset=CardOutline.objects.all(), empty_label="Sélectionnez un contour...",
                                     label='Contour de la carte')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        outline_preview_url = reverse('outline-preview')
        self.fields['outline'].widget.attrs.update({
            'hx-get': outline_preview_url,
            'hx-target': '#outline-preview',
        })


class BaseCardSlotForm(BaseFormSet):
    deletion_widget = forms.HiddenInput()


class CardSlotForm(forms.Form):
    title = forms.CharField(max_length=100, label='Titre du slot')
    image = forms.ModelChoiceField(queryset=CardSlot.objects.all(), empty_label="Sélectionnez un slot...",
                                   label='Slot de la carte')
    size = forms.IntegerField(
        label='Taille du slot (en %)',
        widget=forms.TextInput(
            attrs={
                'type': 'range',
                'min': 1,
                'max': DEFAULT_MAX_SLOT_IMAGE_SIZE,
                'step': 1,
                'value': DEFAULT_SLOT_IMAGE_SIZE
            })
    )

    x_position = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    y_position = forms.FloatField(widget=forms.HiddenInput(), initial=0)

    def __init__(self, *args, **kwargs):
        slot_index = kwargs.pop('slot_index', 0)
        super().__init__(*args, **kwargs)
        slot_preview_url = reverse('slot-preview')
        self.fields['title'].initial = f'Slot {slot_index}'
        self.fields['title'].widget.attrs.update({
            'class': 'slot-title-input',
        })
        self.fields['image'].widget.attrs.update({
            'hx-get': slot_preview_url,
            'hx-target': f'#slot-img-container-{slot_index}',
            'hx-swap': 'innerHTML',
            'hx-vals': json.dumps({'slot_index': str(slot_index)}),
        })
        self.fields['size'].widget.attrs.update({
            'data-slot-id': str(slot_index),
        })
        self.fields['x_position'].name = f'x_position_{slot_index}'
        self.fields['y_position'].name = f'y_position_{slot_index}'


CardSlotFormSet = formset_factory(CardSlotForm, formset=BaseCardSlotForm, extra=0, can_delete=True)
