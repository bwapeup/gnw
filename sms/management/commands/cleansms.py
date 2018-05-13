from django.core.management.base import BaseCommand
from sms.models import SMS_Code, Token, Registration_Token
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):

    help = "Set old sms codes (2+ min old), tokens (11+ min old) and Registration_Tokens (11+ min old) to expired"
    
    def handle(self, *args, **options):
        SMS_Code.objects.filter(expired=False, created__lt=timezone.now()-timedelta(minutes=2)).update(expired=True)
        Token.objects.filter(expired=False, created__lt=timezone.now()-timedelta(minutes=11)).update(expired=True)
        Registration_Token.objects.filter(expired=False, created__lt=timezone.now()-timedelta(minutes=11)).update(expired=True)
        
