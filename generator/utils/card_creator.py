import json

from .image_generator import generate_card_image
from ..models import Card


def create_card(card_name, preset, outline, slots, displayed_width):
    card_image = generate_card_image(outline, slots, displayed_width)

    preset_dict = {
        'name': card_name,
        'outline': outline.id,
        'slots': slots
    }

    card = Card(
        name=card_name,
        image=card_image,
        preset=preset,
        preset_json=json.dumps(preset_dict)
    )
    card.save()
    return card
