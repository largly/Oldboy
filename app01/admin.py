from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(DegreeCourse)
admin.site.register(Teacher)
admin.site.register(PricePolicy)
