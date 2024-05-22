import os
import uuid

from PIL import Image
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

        if 'gem' in slot and slot['gem']:
            gem_image_instance = GemImage.objects.get(id=slot['gem'])
            gem_image = open_image(gem_image_instance.image.path)

            # Resize the gem image to 99% of the slot size
            gem_size = size * GEM_SIZE_RATIO
            gem_image = resize_image(gem_image, gem_size * scale_factor)

            # Calculate the gem position to center it within the slot
            gem_scaled_x_position = scaled_x_position + (slot_image.width - gem_image.width) // 2
            gem_scaled_y_position = scaled_y_position + (slot_image.height - gem_image.height) // 2

            # Paste the gem image onto the base image at the calculated position
            base_image = paste_image(base_image, gem_image, (gem_scaled_x_position, gem_scaled_y_position))

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
