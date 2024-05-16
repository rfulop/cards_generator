from django.urls import path

from .views import OutlinePreviewView, SlotPreviewView, DeleteSlotFormView, CreateSlotFormView, CreateCardView, \
    CardDetailView, GetPresetDetailsView, SaveAsPresetView, CardListView, CardDeleteView

urlpatterns = [
    path('create-card', CreateCardView.as_view(), name='create-card'),
    path('htmx/outline-preview', OutlinePreviewView.as_view(), name='outline-preview'),
    path('htmx/slot-preview', SlotPreviewView.as_view(), name='slot-preview'),
    path('htmx/slot/<int:index>/delete', DeleteSlotFormView.as_view(), name='delete-slot-form'),
    path('htmx/slot/create', CreateSlotFormView.as_view(), name='create-slot-form'),
    path('card/<int:card_id>', CardDetailView.as_view(), name='card-detail'),
    path('card/<int:card_id>/delete/', CardDeleteView.as_view(), name='card-delete'),
    path('preset/<int:preset_id>/details', GetPresetDetailsView.as_view(), name='get-preset-details'),
    path('card/<int:card_id>/save-as-preset', SaveAsPresetView.as_view(), name='save-as-preset'),
    path('cards', CardListView.as_view(), name='card-list'),
]
