from django.contrib import admin
from .models import BillingAddress, Item , OrderItem , Order , Payment
# Register your models here.

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)