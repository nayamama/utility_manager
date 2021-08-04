from django.contrib import admin

from .models import Bill, Utility, Payment

# Register your models here.
admin.site.register(Bill)
admin.site.register(Utility)
admin.site.register(Payment)
