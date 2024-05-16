from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from .constants import DEFAULT_SLOT_IMAGE_SIZE, DISPLAYED_WIDTH
from .forms import CardOutlineSelectionForm, CardSlotForm, CardSlotFormSet, CardDetailsForm
from .models import OutlineImage, SlotImage, Card, CardPreset
from .utils.card_creator import create_card
from .utils.card_preset import create_card_preset_from_json


class HomeView(TemplateView):
    template_name = 'base.html'


class OutlinePreviewView(TemplateView):
    template_name = 'generator/partials/outline_preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outline_id = self.request.GET.get('outline')
        if outline_id:
            context['outline'] = get_object_or_404(OutlineImage, pk=outline_id)
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'outline' not in context:
            return HttpResponse('', status=200)
        return super().render_to_response(context, **response_kwargs)


class SlotPreviewView(TemplateView):
    template_name = 'generator/partials/slot_preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slot_index = self.request.GET.get('slot_index')
        slot_id = self.request.GET.get(f'slots-{slot_index}-image')
        if slot_id:
            context['slot'] = get_object_or_404(SlotImage, pk=slot_id)
            context['slot_index'] = slot_index
            context['size'] = DEFAULT_SLOT_IMAGE_SIZE
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'slot' not in context:
            return HttpResponse('', status=200)
        return super().render_to_response(context, **response_kwargs)


class DeleteSlotFormView(View):
    template_name = 'generator/partials/slot_preview_delete.html'

    def get(self, request, index, *args, **kwargs):
        slot_html = render_to_string(self.template_name, {'slot_index': index})
        return HttpResponse(slot_html, status=200)


class CreateSlotFormView(View):
    template_name_slot_form = 'generator/partials/slot_form.html'
    template_name_management_fields = 'generator/partials/formset_management_fields.html'
    template_name_image_container = 'generator/partials/slot_image_container.html'

    def get(self, request, *args, **kwargs):
        total_forms = int(request.GET.get('total_forms', 0)) + 1
        slot_index = total_forms - 1

        form = CardSlotForm(prefix=f'slots-{slot_index}', slot_index=slot_index)
        formset_class = formset_factory(CardSlotForm, extra=0)
        formset = formset_class(initial=[{}] * total_forms, prefix='slots')
        formset.total_form_count = total_forms

        slot_html = render_to_string(self.template_name_slot_form, {'form': form, 'slot_index': slot_index})
        formset_management_fields_html = render_to_string(self.template_name_management_fields,
                                                          {'formset': formset})
        image_container_html = render_to_string(self.template_name_image_container, {'slot_index': slot_index})

        response_html = slot_html + image_container_html + formset_management_fields_html
        return HttpResponse(response_html, status=200)


class CreateCardView(View):
    template_name = 'generator/create_card.html'
    prefix = 'slots'
    success_message = 'Card created successfully'

    def get(self, request, *args, **kwargs):
        context = {
            'card_details_form': CardDetailsForm(),
            'outline_form': CardOutlineSelectionForm(),
            'slot_formset': CardSlotFormSet(prefix=self.prefix)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        card_details_form = CardDetailsForm(request.POST)
        outline_form = CardOutlineSelectionForm(request.POST)
        slot_formset = CardSlotFormSet(request.POST, prefix=self.prefix)

        if card_details_form.is_valid() and outline_form.is_valid() and slot_formset.is_valid():
            return self.form_valid(request, card_details_form, outline_form, slot_formset)
        else:
            return self.form_invalid(request, card_details_form, outline_form, slot_formset)

    def form_valid(self, request, card_details_form, outline_form, slot_formset):
        card_name = card_details_form.cleaned_data.get('name')
        preset = card_details_form.cleaned_data.get('preset')
        outline = outline_form.cleaned_data.get('outline')
        slots = [
            {
                'title': slot_form.cleaned_data.get('title'),
                'image': slot_form.cleaned_data.get('image').id,
                'size': slot_form.cleaned_data.get('size'),
                'x_position': slot_form.cleaned_data.get('x_position'),
                'y_position': slot_form.cleaned_data.get('y_position')
            }
            for slot_form in slot_formset if slot_form.cleaned_data.get('DELETE') is False
        ]

        card = create_card(card_name, preset, outline, slots, DISPLAYED_WIDTH)
        messages.success(request, self.success_message)
        return redirect('card-detail', card_id=card.id)

    def form_invalid(self, request, card_details_form, outline_form, slot_formset):
        return render(request, self.template_name, {
            'card_details_form': card_details_form,
            'outline_form': outline_form,
            'slot_formset': slot_formset
        })


class CardDetailView(DetailView):
    model = Card
    template_name = 'generator/card_detail.html'
    context_object_name = 'card'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs['card_id'])


class GetPresetDetailsView(View):
    def get(self, request, *args, **kwargs):
        preset = get_object_or_404(CardPreset, pk=self.kwargs['preset_id'])
        slots = list(preset.slots.values('id', 'title', 'image_id', 'size', 'x_position', 'y_position'))
        data = {
            'name': preset.name,
            'outline_id': preset.outline.id,
            'slots': slots,
        }
        return JsonResponse(data)


class SaveAsPresetView(View):
    def post(self, request, *args, **kwargs):
        card = get_object_or_404(Card, pk=self.kwargs['card_id'])
        card_preset = create_card_preset_from_json(card.preset_json)
        card.preset = card_preset
        card.save()
        messages.success(request, 'Card saved as preset successfully')
        return redirect('card-detail', card_id=card.id)


class CardListView(ListView):
    model = Card
    template_name = 'generator/card_list.html'
    paginate_by = 8
