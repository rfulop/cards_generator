import os
import uuid

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

from generator.constants import GEM_SIZE_RATIO
from generator.models import SlotImage, GemImage


def open_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No such file or directory: '{image_path}'")
    return Image.open(image_path).convert("RGBA")


def resize_image(image, size):
    return image.resize((int(size), int(size)), Image.Resampling.LANCZOS)


def paste_image(base_image, image, position):
    base_image.paste(image, position, image)
    return base_image


def save_image(image, image_path):
    image.save(image_path, format='PNG')


def draw_text_on_slot(slot_image, text, slot_width):
    draw = ImageDraw.Draw(slot_image)
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'arial-bold.ttf')
    font = ImageFont.truetype(font_path, int(slot_width / 2))
    text_x_position = slot_image.width / 2
    text_y_position = slot_image.height / 2
    # Custom padding for arial-bold font to center the text
    vertical_padding = 0.10
    text_y_position += text_y_position * vertical_padding
    draw.text((text_x_position, text_y_position), text, fill='white', font=font, anchor='mm', align='center')
    return slot_image


def generate_card_image(outline, slots, displayed_width):
    base_image = open_image(outline.image.path)
    scale_factor = base_image.width / displayed_width

    for slot in slots:
        slot_image_instance = SlotImage.objects.get(id=slot['image'])
        slot_image = open_image(slot_image_instance.image.path)
        size = slot['size']
        slot_image = resize_image(slot_image, size * scale_factor)

        text = slot.get('text', '')
        if text:  # Check if there is text
            slot_image = draw_text_on_slot(slot_image, text, size * scale_factor)

        x_position = slot['x_position']
        y_position = slot['y_position']
        relative_x_position = x_position / displayed_width
        relative_y_position = y_position / (displayed_width * base_image.height / base_image.width)

        scaled_x_position = int(relative_x_position * base_image.width) - slot_image.width // 2
        scaled_y_position = int(relative_y_position * base_image.height) - slot_image.height // 2

        if 'gem' in slot and slot['gem']:
            gem_image_instance = GemImage.objects.get(id=slot['gem'])
            gem_image = open_image(gem_image_instance.image.path)
            gem_size = size * GEM_SIZE_RATIO
            gem_image = resize_image(gem_image, gem_size * scale_factor)
            gem_scaled_x_position = scaled_x_position + (slot_image.width - gem_image.width) // 2
            gem_scaled_y_position = scaled_y_position + (slot_image.height - gem_image.height) // 2
            base_image = paste_image(base_image, gem_image, (gem_scaled_x_position, gem_scaled_y_position))

        base_image = paste_image(base_image, slot_image, (scaled_x_position, scaled_y_position))

    final_image_filename = f'{uuid.uuid4()}.png'
    final_image_path = os.path.join(settings.MEDIA_ROOT, settings.CARD_IMAGE_UPLOAD_PATH, final_image_filename)
    os.makedirs(os.path.dirname(final_image_path), exist_ok=True)
    save_image(base_image, final_image_path)

    final_image_url = os.path.join(settings.CARD_IMAGE_UPLOAD_PATH, final_image_filename)
    return final_image_url
