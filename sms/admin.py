from django.contrib import admin
from sms.models import SMS_Code, Token

admin.site.register(SMS_Code)
admin.site.register(Token)
