from rest_framework import serializers

from . import models
from . import utils

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ['id', 'name', 'description', 'price', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()

    def get_item_name(self, obj):
        return str(obj.item)

    class Meta:
        model = models.OrderItem
        fields = ['item', 'item_name', 'quantity']
        extra_kwargs = {
            'item': {'required': True},
            'quantity': {'required': True},
        } 


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    def create(self, validated_data):
        order = models.Order()
        order.note = validated_data.get('note', '')
        order.save()
        utils.update_order_items(order, validated_data.get('order_items', []))
        return order

    def update(self, instance, validated_data):
        instance.note = validated_data.get('note', '')
        utils.update_order_items(instance, validated_data.get('order_items', []))
        return instance

    class Meta:
        model = models.Order
        fields = ['id', 'note', 'payment_amount', 'order_items']
