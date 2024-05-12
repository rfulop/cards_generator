from django.forms import formset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from .constants import DEFAULT_SLOT_IMAGE_SIZE, DISPLAYED_WIDTH
from .forms import CardOutlineSelectionForm, CardSlotForm, CardSlotFormSet
from .models import CardOutline, CardSlot
from .utils.image_generator import generate_card_image


def get_object_or_404(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404(f'{model.__name__} not found')


def outline_preview(request):
    outline_id = request.GET.get('outline')
    if outline_id:
        outline = get_object_or_404(CardOutline, outline_id)
        return render(request, 'generator/partials/outline_preview.html', {'outline': outline})
    else:
        return HttpResponse('', status=200)


def slot_preview(request):
    slot_index = request.GET.get('slot_index')
    slot_id = request.GET.get(f'slots-{slot_index}-image')
    if slot_id:
        slot = get_object_or_404(CardSlot, slot_id)
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
        outline_form = CardOutlineSelectionForm(request.POST)
        slot_formset = CardSlotFormSet(request.POST, prefix='slots')

        if outline_form.is_valid() and slot_formset.is_valid():
            outline = outline_form.cleaned_data.get('outline')
            slots = [(form.cleaned_data.get('image'), form.cleaned_data.get('size'),
                      form.cleaned_data.get('x_position'), form.cleaned_data.get('y_position'))
                     for form in slot_formset if form.cleaned_data.get('DELETE') is False]

            generate_card_image(outline, slots, DISPLAYED_WIDTH)
        else:
            return render(request, 'generator/create_card.html',
                          {'form': outline_form, 'slot_formset': slot_formset})

    else:
        outline_form = CardOutlineSelectionForm()
        slot_formset = CardSlotFormSet(prefix='slots')

    return render(request, 'generator/create_card.html',
                  {'form': outline_form, 'slot_formset': slot_formset})
