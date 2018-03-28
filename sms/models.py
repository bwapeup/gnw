from django.db import models

#======================================================
#SMS Code
#======================================================
class SMS_Code(models.Model):
    mobile = models.CharField(max_length = 25)
    code = models.CharField(max_length = 7)
    last_update = models.DateTimeField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.mobile
