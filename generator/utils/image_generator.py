import uuid

from PIL import Image
import os
from django.conf import settings


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

    for slot, size, x_position, y_position in slots:
        # Open the slot image
        slot_image = open_image(slot.image.path)

        # Resize the slot image
        slot_image = resize_image(slot_image, size * scale_factor)

        # Calculate the scaled positions
        scaled_x_position = int(x_position * base_image.width) - slot_image.width // 2
        scaled_y_position = int(y_position * base_image.height) - slot_image.height // 2

        # Paste the slot image onto the base image at the scaled position
        base_image = paste_image(base_image, slot_image, (scaled_x_position, scaled_y_position))

    # Save the final image
    final_image_filename = f'{uuid.uuid4()}.png'
    final_image_path = os.path.join(settings.SAVED_CARDS_DIR, final_image_filename)

    # Create the saved cards directory if it doesn't exist
    os.makedirs(settings.SAVED_CARDS_DIR, exist_ok=True)

    save_image(base_image, final_image_path)

    return final_image_path
