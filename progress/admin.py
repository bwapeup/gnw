from django.contrib import admin, messages
from progress.models import Completed_Lessons

"""
Below turns off the bulk-delete option for Completed_Lessons at the Admin site.
To delete a completed lesson record, you must call the instance's delete() method,
which is overridden to raise exception if the record is related to a submitted assignment.
Bulk delete would just call the delete method of the QuerySet, bypassing this restriction.
Note that this does not stop you from doing bulk delete programmatically elsewhere. So be careful!
"""
class Completed_LessonsAdmin(admin.ModelAdmin):

    def delete_model(self, request, obj):
        if obj.assignment:
            messages.add_message(request, messages.ERROR, 'Attention!!!! "' + obj.__str__() + '" was not deleted. It is related to a submitted assignment')
            messages.add_message(request, messages.ERROR, 'Please ignore the auto-generated success message below. It is not accurate.')
        else:
            super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        num_obj_not_deleted = 0
        for obj in queryset:
            if obj.assignment:
                num_obj_not_deleted += 1
                messages.add_message(request, messages.ERROR, 'Attention!!!! "' + obj.__str__() + '" was not deleted. It is related to a submitted assignment')
            else:
                obj.delete()
            if num_obj_not_deleted > 0:
                messages.add_message(request, messages.ERROR, 'A total of ' + str(num_obj_not_deleted) + ' records were NOT deleted. Subtract this number from the inaccurate success message below.')


admin.site.register(Completed_Lessons, Completed_LessonsAdmin)
