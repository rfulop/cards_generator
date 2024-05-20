from django.urls import path

from .views import CardDetailView, CardDeleteView, CardListView, CardCreateView, OutlinePreviewView, \
    SlotPreviewView, DeleteSlotFormView, CreateSlotFormView, GetPresetDetailsView, SaveAsPresetView, CardUpdateView

urlpatterns = [
    path('', CardCreateView.as_view(), name='card-create'),
    path('create-card/', CardCreateView.as_view(), name='create-card'),
    path('htmx/outline-preview/', OutlinePreviewView.as_view(), name='outline-preview'),
    path('htmx/slot-preview/', SlotPreviewView.as_view(), name='slot-preview'),
    path('htmx/slot/<int:index>/delete/', DeleteSlotFormView.as_view(), name='delete-slot-form'),
    path('htmx/slot/create/', CreateSlotFormView.as_view(), name='create-slot-form'),
    path('cards/', CardListView.as_view(), name='card-list'),
    path('card/<int:card_id>/', CardDetailView.as_view(), name='card-detail'),
    path('card/<int:card_id>/delete/', CardDeleteView.as_view(), name='card-delete'),
    path('preset/<int:preset_id>/details/', GetPresetDetailsView.as_view(), name='preset-details'),
    path('card/<int:card_id>/save-as-preset/', SaveAsPresetView.as_view(), name='save-as-preset'),
    path('card/<int:card_id>/update/', CardUpdateView.as_view(), name='card-update'),
]
