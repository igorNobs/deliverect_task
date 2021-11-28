from django.db import transaction
from rest_framework import serializers

from . import models


def _restore_menu_availability(item_list):
    for i in item_list:
        menu_item = i.item
        quantity = i.quantity
        menu_item.quantity += quantity
        menu_item.save()


def _subtract_item_availability(menu_item, quantity):
    menu_item.quantity -= quantity
    menu_item.save()


@transaction.atomic
def update_order_items(order_instance, items_list):
    '''
        Atomic function to update order items and price, performs following logic:
            1. if order had any items, delete them from order and put them back in stock
            2. validate if stock has enough items to fill the order request
            3. add requested items to the order
            4. reduce the number of items in stock accordingly
            5. update payment amount accordingly
    '''
    order_instance.payment_amount = 0
    order_items = order_instance.order_items.all()
    if order_items.count():
        _restore_menu_availability(order_items)
        order_items.delete()
    new_order_items = []
    for i in items_list:
        order_item = models.OrderItem()
        order_item.item = models.MenuItem.objects.get(pk=i['item'].pk)
        order_item.quantity = i['quantity']
        order_item.order = order_instance
        if (order_item.item.quantity - order_item.quantity) < 0:
            raise serializers.ValidationError('not enough "{}" in stock'.format(order_item.item.name))
        new_order_items.append(order_item)
        _subtract_item_availability(order_item.item, order_item.quantity)
        order_instance.payment_amount += (order_item.item.price * order_item.quantity)
    models.OrderItem.objects.bulk_create(new_order_items)
    order_instance.save()
