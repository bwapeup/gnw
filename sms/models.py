from django.db import models

#======================================================
#SMS Code
#======================================================
class SMS_Code(models.Model):
    mobile = models.CharField(max_length = 25)
    code = models.CharField(max_length = 7)
    created = models.DateTimeField()
    verified = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    tries = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.mobile

class Token(models.Model):
    mobile = models.CharField(max_length = 25)
    session_key = models.CharField(null=False, max_length=40)
    token_hex_str = models.CharField(max_length = 32)
    created = models.DateTimeField()
    verified = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.token_hex_str
