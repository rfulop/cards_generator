from django.contrib import admin

from .models import CardOutline, CardSlot


@admin.register(CardOutline)
class CardOutlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(CardSlot)
class CardSlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
