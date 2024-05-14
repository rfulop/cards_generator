from django.contrib import admin

from .models import OutlineImage, SlotImage


@admin.register(OutlineImage)
class CardOutlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(SlotImage)
class CardSlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
