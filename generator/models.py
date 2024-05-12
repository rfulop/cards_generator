from django.db import models


class CardOutline(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='assets/card_outlines/')

    def __str__(self):
        return self.name


class CardSlot(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='assets/card_slots/')

    def __str__(self):
        return self.name
