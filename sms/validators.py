from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class AtLeastOneNumberPasswordValidator:
    """
    Validate whether the password contains at least 1 number.
    """
    def validate(self, password, user=None):
        if not re.match(r'.*[0-9].*', password):
            raise ValidationError("密码必须包含至少一个数字")

    def get_help_text(self):
        return _("Your password must contain at least 1 number.")
