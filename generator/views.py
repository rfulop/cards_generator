import json

from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .constants import DEFAULT_SLOT_IMAGE_SIZE, DISPLAYED_WIDTH
from .forms import CardOutlineSelectionForm, CardSlotForm, CardSlotFormSet, CardDetailsForm
from .models import OutlineImage, SlotImage, Card
from .utils.image_generator import generate_card_image
from .utils.card_utils import prepare_slots_for_json


def get_object_or_404(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404(f'{model.__name__} not found')


def outline_preview(request):
    outline_id = request.GET.get('outline')
    if outline_id:
        outline = get_object_or_404(OutlineImage, outline_id)
        return render(request, 'generator/partials/outline_preview.html', {'outline': outline})
    else:
        return HttpResponse('', status=200)


def slot_preview(request):
    slot_index = request.GET.get('slot_index')
    slot_id = request.GET.get(f'slots-{slot_index}-image')
    if slot_id:
        slot = get_object_or_404(SlotImage, slot_id)
        return render(request, 'generator/partials/slot_preview.html',
                      {'slot': slot, 'slot_index': slot_index, 'size': DEFAULT_SLOT_IMAGE_SIZE})
    else:
        return HttpResponse('', status=200)


def delete_slot_form(request, index):
    slot_html = render_to_string('generator/partials/slot_preview_delete.html',
                                 {'slot_index': index})
    return HttpResponse(slot_html, status=200)


def create_slot_form(request):
    total_forms = int(request.GET.get('total_forms', 0)) + 1
    slot_index = total_forms - 1

    form = CardSlotForm(prefix=f'slots-{slot_index}', slot_index=slot_index)

    slot_html = render_to_string('generator/partials/slot_form.html',
                                 {'form': form, 'slot_index': slot_index})

    formset_class = formset_factory(CardSlotForm, extra=0)
    formset = formset_class(initial=[{}] * total_forms, prefix='slots')

    formset.total_form_count = total_forms

    formset_management_fields_html = render_to_string('generator/partials/formset_management_fields.html',
                                                      {'formset': formset})

    image_container_html = render_to_string('generator/partials/slot_image_container.html',
                                            {'slot_index': slot_index})

    response_html = slot_html + image_container_html + formset_management_fields_html
    return HttpResponse(response_html, status=200)


def create_card(request):
    if request.method == 'POST':
        card_details_form = CardDetailsForm(request.POST)
        outline_form = CardOutlineSelectionForm(request.POST)
        slot_formset = CardSlotFormSet(request.POST, prefix='slots')

        if card_details_form.is_valid() and outline_form.is_valid() and slot_formset.is_valid():
            card_name = card_details_form.cleaned_data.get('name')
            outline = outline_form.cleaned_data.get('outline')
            slots = [(form.cleaned_data.get('image'), form.cleaned_data.get('size'),
                      form.cleaned_data.get('x_position'), form.cleaned_data.get('y_position'))
                     for form in slot_formset if form.cleaned_data.get('DELETE') is False]

            card_image = generate_card_image(outline, slots, DISPLAYED_WIDTH)

            preset = {
                'outline': outline.id,
                'slots': prepare_slots_for_json(slots)
            }
            preset_json = json.dumps(preset)

            card = Card(
                name=card_name,
                image=card_image,
                preset=preset_json
            )
            card.save()

            messages.success(request, 'Card created successfully')
            return redirect('card-detail', pk=card.id)
        else:
            return render(request, 'generator/create_card.html',
                          {'card_details_form': card_details_form, 'outline_form': outline_form,
                           'slot_formset': slot_formset})

    else:
        card_details_form = CardDetailsForm()
        outline_form = CardOutlineSelectionForm()
        slot_formset = CardSlotFormSet(prefix='slots')

    return render(request, 'generator/create_card.html',
                  {'card_details_form': card_details_form, 'outline_form': outline_form,
                   'slot_formset': slot_formset})


def card_detail(request, pk):
    card = get_object_or_404(Card, pk)
    return render(request, 'generator/card_detail.html', {'card': card})

