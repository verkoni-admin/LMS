from django.core.exceptions import ValidationError
from .utils import MAX_PROFILE_PIC_SIZE, MAX_LECTURE_ATTACHMENT_FILE_SIZE


def validate_image_size(image):

    if image.size > MAX_PROFILE_PIC_SIZE:
        raise ValidationError("Maximum size allowed for profile pic is 5MB")

def validate_lecture_attachment_size(attachment):

    if attachment.size > MAX_LECTURE_ATTACHMENT_FILE_SIZE:
        raise ValidationError("Maximum size allowed for lecture attachment is 20MB")

