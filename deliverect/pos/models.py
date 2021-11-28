from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False, default=1)

    def __str__(self):
        return self.name


class Order(models.Model):
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False, default=0)
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return 'Order # {}'.format(self.pk)


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=False, related_name='order_items')
    quantity = models.IntegerField(blank=False, null=False, default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')

    def __str__(self):
        return '{} -  {} ({})'.format(self.order, self.item, self.quantity)
