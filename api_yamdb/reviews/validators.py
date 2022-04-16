from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_me(value):
    if value == 'me':
        raise ValidationError(
            (_('It is forbidden to take the username "me"')),
            params={'value': value},
        )
