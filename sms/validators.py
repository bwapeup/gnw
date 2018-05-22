from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class AllLettersPasswordValidator:
    """
    Validate whether the password is consisted of all letters.
    """
    def validate(self, password, user=None):
        if not re.match(r'.*[0-9].*', password):
            raise ValidationError(
                _("密码必须包含一个数字"),
                code='password_entirely_alpha',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 number.")
