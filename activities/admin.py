from django.contrib import admin
from .models import Activity, Course


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'course_code',
        'friendly_name',
        'name',
        'activity',
        'price',
        'length',
        'solo',
        'incl_cert',
    )

    ordering = ('course_code', 'activity',)


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Course, CourseAdmin)
