from django.urls import path

from .views import (create_card, outline_preview, slot_preview, create_slot_form, delete_slot_form, card_detail,
                    save_as_preset, get_preset_details)

urlpatterns = [
    path('', create_card, name='create-card'),
    path('create-card', create_card, name='create-card'),
    path('htmx/outline-preview', outline_preview, name='outline-preview'),
    path('htmx/slot-preview', slot_preview, name='slot-preview'),
    path('htmx/slot/create', create_slot_form, name='create-slot-form'),
    path('htmx/slot/<int:index>/delete', delete_slot_form, name='delete-slot-form'),
    path('card-detail/<int:card_id>', card_detail, name='card-detail'),
    path('save-as-preset/<int:card_id>', save_as_preset, name='save-as-preset'),
    path('presets/<int:preset_id>', get_preset_details, name='get-preset-details'),
]
