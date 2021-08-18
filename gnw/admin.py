from django.contrib import admin
from .models import Course, Unit, Lesson, Video, Quiz, Quiz_Question

# Register your models here.
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Quiz)
admin.site.register(Quiz_Question)





