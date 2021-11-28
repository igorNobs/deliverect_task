from rest_framework import status
from rest_framework.test import APITestCase

from . import models


class TestMenuOperations(APITestCase):
    def setUp(self):
        self.menu_url = '/pos/menu/'
        self.item = {
            'name': 'Pasta Fetuccini',
            'description': 'Eat pasta, grow fasta',
            'price': 18.99,
            'quantity': 10,
        }
        self.item_updated = {
            'name': 'Pasta Alfredo',
            'description': 'Eat pasta, grow fasta',
            'price': 18.99,
            'quantity': 20,
        }

    def test_menu_item_creation(self):
        response = self.client.post(self.menu_url, self.item, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.MenuItem.objects.count(), 1)
        self.assertEqual(models.MenuItem.objects.get().name, self.item['name'])

    def test_menu_retrieval(self):
        self.client.post(self.menu_url, self.item, format='json')
        response = self.client.get(self.menu_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_menu_item_update(self):
        create_response = self.client.post(self.menu_url, self.item, format='json')
        id = create_response.data['id']
        update_url = '{}{}/'.format(self.menu_url, id)
        update_response = self.client.put(update_url, self.item_updated, format='json')
        self.assertEqual(update_response.data['id'], id)
        self.assertEqual(update_response.data['name'], self.item_updated['name'])
        self.assertEqual(update_response.data['quantity'], self.item_updated['quantity'])

    def test_menu_item_destroy(self):
        create_response = self.client.post(self.menu_url, self.item, format='json')
        id = create_response.data['id']
        self.assertEqual(models.MenuItem.objects.count(), 1)
        destroy_url = '{}{}/'.format(self.menu_url, id)
        destroy_response = self.client.delete(destroy_url)
        self.assertEqual(destroy_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.MenuItem.objects.count(), 0)


class TestOrderOperations(APITestCase):
    def setUp(self):
        self.menu_url = '/pos/menu/'
        self.order_url = '/pos/order/'
        self.item1 = {
            'name': 'Pasta Fetuccini',
            'description': 'Eat pasta, grow fasta',
            'price': 18.99,
            'quantity': 10,
        }
        self.item2 = {
            'name': 'Pasta Alfredo',
            'description': 'Eat pasta, grow fasta',
            'price': 18.99,
            'quantity': 20,
        }
        self.order = {
            "note": "Leave order at the door",
            "order_items": [
                {
                    "item": 1,
                    "quantity": 2
                },
                {
                    "item": 2,
                    "quantity": 1
                }
            ]
        }
        self.order_updated = {
            "note": "Leave order at the door",
            "order_items": [
                {
                    "item": 1,
                    "quantity": 5
                },
                {
                    "item": 2,
                    "quantity": 5
                }
            ]
        }
        self.client.post(self.menu_url, self.item1, format='json')
        self.client.post(self.menu_url, self.item2, format='json')
    
    def test_order_creation(self):
        response = self.client.post(self.order_url, self.order, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Order.objects.count(), 1)
        order = models.Order.objects.get()
        self.assertEqual(order.note, self.order['note'])
        self.assertEqual(order.order_items.count(), 2)
        self.assertEqual(float(order.payment_amount), 56.97)

        menu_item1 = models.MenuItem.objects.get(pk=1)
        menu_item2 = models.MenuItem.objects.get(pk=2)
        self.assertEqual(menu_item1.quantity, 8)
        self.assertEqual(menu_item2.quantity, 19)

    def test_order_update(self):
        response = self.client.post(self.order_url, self.order, format='json')
        id = response.data['id']
        order = models.Order.objects.get()
        update_url = '{}{}/'.format(self.order_url, id)
        update_response = self.client.put(update_url, self.order_updated, format='json')
        self.assertEqual(update_response.data['id'], id)
        self.assertEqual(order.order_items.count(), 2)
        menu_item1 = models.MenuItem.objects.get(pk=1)
        menu_item2 = models.MenuItem.objects.get(pk=2)
        self.assertEqual(menu_item1.quantity, 5)
        self.assertEqual(menu_item2.quantity, 15)
