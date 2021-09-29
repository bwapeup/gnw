from django.contrib import admin, messages
from enrollment.models import Enrollment, Process_New_Order

#Below adds a bulk action option on the admin page for the Process_New_Order model
@admin.action(description='Process Selected Orders')
def process_new_orders(modeladmin, request, queryset):
    processed = 0
    failures = 0
    successes = 0

    for new_order in queryset:
        if not new_order.processed:
            new_order.process_order()
            processed += 1
            if new_order.failure_details:
                failures += 1
                messages.error(request, str(new_order) + ': There were errors! Click on the item for details.')
            else:
                successes += 1
                messages.success(request, str(new_order) + ': processed successfully.')
    if processed == 0:
        messages.warning(request, 'Warning! No orders were processed. The selected orders were all marked as processed already.')
    else:
        msg = 'Batches selected: '+str(len(queryset))+ '; Batches processed: ' + str(processed)+ '; Failed: '+str(failures)+ '; Succeeded: '+str(successes)
        if failures > 0:
            messages.error(request, msg)
        else:
            messages.info(request, msg)

class EnrollmentAdmin(admin.ModelAdmin):
    actions = [process_new_orders]

admin.site.register(Enrollment)
admin.site.register(Process_New_Order, EnrollmentAdmin)