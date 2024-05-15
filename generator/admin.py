from django.contrib import admin

from .models import OutlineImage, SlotImage, CardSlot, CardPreset, Card


@admin.register(OutlineImage)
class CardOutlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(SlotImage)
class CardSlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(CardSlot)
class CardSlotAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'size', 'x_position', 'y_position')


@admin.register(CardPreset)
class CardPresetAdmin(admin.ModelAdmin):
    list_display = ('name', 'outline')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'preset_json', 'preset')
