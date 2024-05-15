import os
import uuid

from PIL import Image
from django.conf import settings

from generator.models import SlotImage


def open_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No such file or directory: '{image_path}'")
    return Image.open(image_path)


def resize_image(image, size):
    return image.resize((int(size), int(size)))


def paste_image(base_image, image, position):
    base_image.paste(image, position, image)
    return base_image


def save_image(image, image_path):
    image.save(image_path, format='PNG')


def generate_card_image(outline, slots, displayed_width):
    # Open the base image
    base_image = open_image(outline.image.path)

    # Calculate the scale factor
    scale_factor = base_image.width / displayed_width

    for slot in slots:
        # Open the slot image
        slot_image_instance = SlotImage.objects.get(id=slot['image'])
        slot_image = open_image(slot_image_instance.image.path)

        # Resize the slot image
        size = slot['size']
        slot_image = resize_image(slot_image, size * scale_factor)

        # Calculate the scaled positions
        x_position = slot['x_position']
        y_position = slot['y_position']
        scaled_x_position = int(x_position * base_image.width) - slot_image.width // 2
        scaled_y_position = int(y_position * base_image.height) - slot_image.height // 2

        # Paste the slot image onto the base image at the scaled position
        base_image = paste_image(base_image, slot_image, (scaled_x_position, scaled_y_position))

    # Save the final image
    final_image_filename = f'{uuid.uuid4()}.png'
    final_image_path = os.path.join(settings.MEDIA_ROOT, settings.CARD_IMAGE_UPLOAD_PATH, final_image_filename)

    # Create the saved cards directory if it doesn't exist
    os.makedirs(os.path.dirname(final_image_path), exist_ok=True)

    save_image(base_image, final_image_path)

    final_image_url = os.path.join(settings.CARD_IMAGE_UPLOAD_PATH, final_image_filename)
    return final_image_url
