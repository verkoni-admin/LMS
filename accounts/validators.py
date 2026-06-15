from django.core.exceptions import ValidationError
from .utils import MAX_PROFILE_PIC_SIZE


def validate_image_size(image):

    if image.size > MAX_PROFILE_PIC_SIZE:
        raise ValidationError("Maximum size allowed for profile pic is 5MB")
