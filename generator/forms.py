import json

from django import forms
from django.conf import settings
from django.forms import formset_factory, BaseFormSet
from django.urls import reverse

from .constants import DEFAULT_SLOT_IMAGE_SIZE, DEFAULT_MAX_SLOT_IMAGE_SIZE
from .models import OutlineImage, SlotImage, GemImage, CardPreset


class CardDetailsForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nom de la carte')
    preset = forms.ModelChoiceField(queryset=CardPreset.objects.all(),
                                    empty_label="Vous pouvez sélectionner un preset...", required=False)


class CardOutlineSelectionForm(forms.Form):
    outline = forms.ModelChoiceField(queryset=OutlineImage.objects.all(), empty_label="Sélectionnez un contour...",
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
    image = forms.ModelChoiceField(queryset=SlotImage.objects.all(), empty_label="Sélectionnez un slot...",
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
    gem = forms.ModelChoiceField(queryset=GemImage.objects.all(), empty_label="Sélectionnez une gemme...",
                                 label='Gemme', required=False)
    text = forms.CharField(max_length=8, label='Texte', required=False)
    font = forms.ChoiceField(choices=[(k, k) for k in settings.AVAILABLE_FONTS.keys()], label='Police', required=False,
                             initial=settings.DEFAULT_SLOT_FONT)
    text_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}), label='Couleur du texte',
                                 required=False, initial=settings.DEFAULT_SLOT_TEXT_COLOR)

    def __init__(self, *args, **kwargs):
        slot_index = kwargs.pop('slot_index', 0)
        super().__init__(*args, **kwargs)
        slot_preview_url = reverse('slot-preview')
        gem_preview_url = reverse('gem-preview')
        text_preview_url = reverse('slot-text-preview')
        self.fields['title'].initial = f'Slot {slot_index}'
        self.fields['title'].widget.attrs.update({
            'class': 'slot-title-input',
        })
        self.fields['image'].widget.attrs.update({
            'hx-get': slot_preview_url,
            'hx-target': f'#slot-img-container-{slot_index}',
            'hx-swap': 'innerHTML',
            'hx-vals': json.dumps({'slot_index': str(slot_index)}),
            'data-slot-id': str(slot_index),
        })
        self.fields['size'].widget.attrs.update({
            'data-slot-id': str(slot_index),
            'class': 'slot-size-input',
        })
        self.fields['x_position'].name = f'x_position_{slot_index}'
        self.fields['y_position'].name = f'y_position_{slot_index}'
        self.fields['gem'].widget.attrs.update({
            'hx-get': gem_preview_url,
            'hx-target': f'#gem-img-container-{slot_index}',
            'hx-swap': 'innerHTML',
            'hx-vals': json.dumps({'slot_index': str(slot_index)}),
            'data-slot-id': str(slot_index),
        })
        self.fields['text'].widget.attrs.update({
            'hx-get': text_preview_url,
            'hx-target': f'#slot-text-container-{slot_index}',
            'hx-trigger': 'keyup changed delay:500ms, change',
            'hx-vals': json.dumps({'slot_index': str(slot_index)}),
            'data-slot-id': str(slot_index),
        })


CardSlotFormSet = formset_factory(CardSlotForm, formset=BaseCardSlotForm, extra=0, can_delete=True)
