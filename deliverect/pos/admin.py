from django.contrib import admin

from .models import MenuItem, OrderItem, Order


admin.site.register(MenuItem)
admin.site.register(OrderItem)
admin.site.register(Order)
