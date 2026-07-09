from collections.abc import Callable

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


# Option 1
def validate_name(value: str) -> None:
    for char in value:
        if not (char.isalpha() or char.isspace()):
            raise ValidationError("Name can only contain letters and spaces")

# Option 2
def validate_name_2(message: str) -> Callable:
    def validator(value: str) -> None:
        for char in value:
            if not (char.isalpha() or char.isspace()):
                raise ValidationError(message)

    return validator

# Option 3:
@deconstructible
class NameValidator:
    DEFAULT_MESSAGE: str = "Name can only contain letters and spaces"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not isinstance(value, str):
            raise ValueError("Message should be of type str")

        self.__message = value

    def __call__(self, value):
        for char in value:
            if not (char.isalpha() or char.isspace()):
                raise ValidationError(self.message)
