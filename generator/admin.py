from django.contrib import admin

from .models import OutlineImage, SlotImage, CardSlot, CardPreset, Card, GemImage


@admin.register(OutlineImage)
class CardOutlineImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(SlotImage)
class CardSlotImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(GemImage)
class GemImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(CardSlot)
class CardSlotAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'size', 'x_position', 'y_position', 'gem', 'text', 'font')


@admin.register(CardPreset)
class CardPresetAdmin(admin.ModelAdmin):
    list_display = ('name', 'outline')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'preset_json', 'preset')
