import json

from generator.models import CardPreset, CardSlot, SlotImage, OutlineImage, GemImage


def create_card_preset_from_json(preset_json_str):
    preset_json = json.loads(preset_json_str)
    card_preset = CardPreset.objects.create(
        name=preset_json['name'],
        outline=OutlineImage.objects.get(id=preset_json['outline']),
    )

    for slot_json in preset_json['slots']:
        slot = CardSlot.objects.create(
            title=slot_json['title'],
            image=SlotImage.objects.get(id=slot_json['image']),
            size=slot_json['size'],
            x_position=slot_json['x_position'],
            y_position=slot_json['y_position'],
            gem=GemImage.objects.get(id=slot_json['gem']) if 'gem' in slot_json else None,
            text=slot_json['text'] if 'text' in slot_json else None,
            font=slot_json['font'] if 'font' in slot_json else None,
            text_color=slot_json['text_color'] if 'text_color' in slot_json else None,
        )
        card_preset.slots.add(slot)

    return card_preset
