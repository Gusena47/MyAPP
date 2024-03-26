from random import choices
from string import ascii_letters

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse

from shopppCat.models import Product, Order


class OrderDetailsViewTestCase(TestCase):
    fixtures = [
        "order-fixtures.json",
        "product-fixtures.json",
        "user-fixtures.json",
    ]
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='test',
            password='<PASSWORD>',
            email='<EMAIL>',
        )
        cls.group, created = Group.objects.get_or_create(
            name='profile_manager',
        )
        cls.permission = Permission.objects.get(
            codename="view_order",
        )
        cls.user.groups.add(cls.group)
        cls.user.user_permissions.add(cls.permission)
        cls.user.save()
    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="ul Pushkina, d 1",
            promo_code="qwerty", user=self.user, )

    @classmethod
    def tearDownClass(cls) -> None:
        # cls.order.delete()
        cls.user.delete()
        cls.group.delete()

        super().tearDownClass()

    def test_get_order(self):
        response = self.client.get(
            reverse(
                'shopppCat:order-detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'shopppCat/order_detail.html')

    def test_get_order_and_check_content(self):
        response = self.client.get(reverse('shopppCat:order-detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'shopppCat/order_detail.html')
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promo_code)


class OrderExportViewTestCase(TestCase):
    fixtures = [
        "order-fixtures.json",
        "product-fixtures.json",
        "user-fixtures.json",
    ]
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='s', password='bfvhffr',)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()



    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_order_view(self):
        response = self.client.get(reverse('shopppCat:order-export'))
        self.assertEqual(response.status_code, 200)
        order = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promo_code': order.promo_code,
                'user': order.user.username,
                'products': [
                    {
                        'name': product.name,
                        'price': product.price,
                        'discount': product.discount}
                    for product in order.products.all()
                ]
            }
            for order in order
        ]

        order_data = response.json()
        self.assertEqual(order_data['order'], expected_data)