from django.db import models

#======================================================
#SMS Code
#======================================================
class SMS_Code(models.Model):
    """
    The code is a 7-digit numeric sequence using digits
    0-9. As such, there are ten million possibilities.
    The "tries" field helps to protect against brute force
    guessing. Currently, in the view, the threshhold is set at 3.
    After 3 guesses, this sms code is voided and the user must
    get another one for this mobile number. This means
    there is only a probability of 3 in 10 million that an attacker
    will guess the code correctly.
    """
    mobile = models.CharField(max_length = 25)
    code = models.CharField(max_length = 7)
    created = models.DateTimeField()
    verified = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    tries = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.mobile

class Token(models.Model):
    """
    This token is used to reset user passwords.
    This has to be used during the same session, that is
    if the user logs out and then logs back in, this
    token is voided. The "created" field is used to set
    a further restriction on by when it must be used.
    """
    mobile = models.CharField(max_length = 25)
    session_key = models.CharField(null=False, max_length=40)
    token_hex_str = models.CharField(max_length = 32)
    created = models.DateTimeField()
    verified = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.token_hex_str


class Registration_Token(models.Model):
    """
    This token is used to activate new users. It is used
    in the one-time url to submit SMS verification code,
    as well as in the url used by AJAX to request the
    SMS code. Unlike the above token, it does not track
    the user session, which is not available to inactive users.
    """
    mobile = models.CharField(max_length = 25)
    token_hex_str = models.CharField(max_length = 32)
    created = models.DateTimeField()
    sms_sent = models.PositiveSmallIntegerField(default=0)
    verified = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.token_hex_str
