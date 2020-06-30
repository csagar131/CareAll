from django.contrib import admin
from caremain.models import CareRequests,Transaction,Review

admin.site.register(CareRequests)
admin.site.register(Transaction)
admin.site.register(Review)