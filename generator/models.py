from django.conf import settings
from django.db import models


class OutlineImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='assets/card_outlines/')

    def __str__(self):
        return self.name


class SlotImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='assets/card_slots/')

    def __str__(self):
        return self.name


class GemImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='assets/gem_slots/')

    def __str__(self):
        return self.name


class CardSlot(models.Model):
    title = models.CharField(max_length=100)
    image = models.ForeignKey(SlotImage, on_delete=models.CASCADE)
    size = models.IntegerField()
    x_position = models.FloatField()
    y_position = models.FloatField()
    gem = models.ForeignKey(GemImage, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class CardPreset(models.Model):
    name = models.CharField(max_length=100)
    outline = models.ForeignKey(OutlineImage, on_delete=models.CASCADE)
    slots = models.ManyToManyField(CardSlot)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=settings.CARD_IMAGE_UPLOAD_PATH)
    preset_json = models.JSONField(null=True, blank=True)
    preset = models.ForeignKey(CardPreset, on_delete=models.SET_NULL, null=True, blank=True, related_name='cards')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
