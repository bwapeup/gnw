from django.core.management.base import BaseCommand
from sms.models import SMS_Code, Token
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):

    help = "Set old sms codes (3+ min old) and tokens (10+ min old) to expired"
    
    def handle(self, *args, **options):
        SMS_Code.objects.filter(expired=False, created__lt=timezone.now()-timedelta(minutes=3)).update(expired=True)
        Token.objects.filter(expired=False, created__lt=timezone.now()-timedelta(minutes=10)).update(expired=True)
        
