from django.contrib import admin
from sms.models import SMS_Code, Token, Registration_Token

admin.site.register(SMS_Code)
admin.site.register(Token)
admin.site.register(Registration_Token)
