import re

from django.conf import settings
from django.core.exceptions import ValidationError


def hex_validation(value):
    """Валидатор для проверки паттерна HEX кода."""
    pattern = settings.COLOR_REGEX
    if not re.search(pattern, value):
        raise ValidationError("HEX код должен содержать 7 символов, включая #")
