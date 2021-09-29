import re
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import models
from django.conf import settings
from gnw.models import Course
from sms.helpers import send_sms

User = get_user_model()

    
#======================================================
#Enrollment:
#======================================================
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    enrollment_date = models.DateField(default=date.today)

    ENROLLMENT_TYPES = [
        ('TRIAL', 'Trial'),
        ('REGULAR', 'regular'),
    ]

    enrollment_type = models.CharField(max_length = 100, choices=ENROLLMENT_TYPES)
    is_current = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], condition=Q(is_current=True), name='unique_user_enrolled_in_current_course'),
        ]

    def clean(self):
        """
        This is called by ModelForm when saving through ModelForm (e.g. Admin site).
        Be sure to call full_clean() if creating enrollments programmatically.
        """
        if self.is_current == True:
            if Enrollment.objects.filter(user=self.user, course=self.course, is_current=True).exclude(id=self.id).exists():
                raise ValidationError('The user is currently enrolled in this course already.')

    def __str__(self):
        if self.is_current:
            status = 'current'
        else:
            status = 'past'
        return self.user.username + ' ' + self.course.course_name + ' ' + status


#======================================================
#Process_New_Order
#====================================================== 
class Process_New_Order(models.Model):
    """
    Each object of this model is used to process new sales that have occurred on
    our third-party ecommerce platform. The model takes a json list of objects, each
    of which represents a new sale. Each object in this list should contain a
    (1). mobile number,  a (2). course slug, and an (3). enrollment type.
    This json field should be pasted in on the admin page. 
    The model methods should (1). Create or get a new user account for the mobile phone, 
    if it doesn't exist already; (2). Enroll the user in the course(s) purchased; 
    (3). Send a text message to the user's mobile phone, and the message should
    depend on whether it's a new user or a repeat customer.
    """
    order_details = models.JSONField()
    processed = models.BooleanField(default=False)
    failure_details = models.TextField(blank=True)

    @staticmethod
    def create_username():
        while True:
            username = 'autouser' + get_random_string(8, '0123456789')
            if not User.objects.filter(username=username).exists():
                break
        return username

    @staticmethod
    def create_password():
        password = 'x4k' + get_random_string(5, '23456789')
        return password

    @staticmethod
    def enroll_in_course(order):
        """
        The code below makes it possible for a user to enroll in the same course twice, once as a regular
        enrollment and another as a trial enrollment. This is probably not what we want, but without
        knowing exactly what our trial vs regular enrollment policies are, we should not waste 
        our time now. Once we have decided on the details, we need to update the business logic here.
        """
        user = order['user']
        slug = order['course_slug']
        course = Course.objects.filter(slug=slug).get()
        etype = order['enrollment_type']
        enrollment, created = Enrollment.objects.get_or_create(user=user, course=course, enrollment_type=etype, is_current=True)
        return enrollment

    def process_order(self):
        order_details = self.order_details
        errors = ''

        #order_details must be a list of objects
        for order in order_details: 
            mobile = order['mobile']
            defaults = {}
            username = Process_New_Order.create_username()
            defaults.update({'username': username})
            defaults.update({'require_password_change': True})

            try:
                user, created = User.objects.get_or_create(mobile=mobile, defaults=defaults)
            except Exception:
                errors += mobile + ': Failed to find or create account. \n'
                continue
            else:
                if created:
                    password = Process_New_Order.create_password()
                    user.set_password(password)
                    user.save()
                    msg = '【飞猫星球】您购买的课程已开通 请登陆网址：www.feimao.com 用户名：手机号，临时密码：' + password
                else:
                    msg = '【飞猫星球】您购买的课程已开通 请登陆网址：www.feimao.com 用户名：手机号，如您已忘记密码 可重新设置'

            order_info = {}
            order_info.update({'user':user})
            order_info.update({'course_slug':order['course_slug']})
            order_info.update({'enrollment_type':order['enrollment_type']})

            try:
                enrollment = self.enroll_in_course(order_info)
            except Exception:
                errors += mobile + ': Failed to enroll in course ('+order["course_slug"]+') \n'
                continue

            try:
                sms_sent = send_sms(mobile, msg)
            except Exception:
                errors += mobile + ': Failed to send sms. \n'
                continue

        if errors != '':
            self.failure_details = errors
        self.processed = True
        self.save(update_fields=['failure_details', 'processed'])

    def clean(self):
        """
        (1). Verify the mobile number is legit, using regex
        (2). Verify the course identifier is legit, the course really exists
        (3). Verify the enrollment type is legit
        """
        order_details = self.order_details
        for order in order_details:
            mobile = order['mobile']
            if not re.match(r'^[1][0-9]{10}$', mobile):
                raise ValidationError(mobile + ' is not a legitimate Chinese mobile number')

            slug = order['course_slug']
            if not Course.objects.filter(slug=slug).exists():
                raise ValidationError('Course "' +slug + '" does not exist')

            etype = order['enrollment_type']
            if etype != 'REGULAR' and etype != 'TRIAL':
                raise ValidationError('enrollment_type "' +etype + '" is not a legitimate enrollment type (case sensitive)')
