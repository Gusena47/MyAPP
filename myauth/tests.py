import json

from django.test import TestCase
from django.urls import reverse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('myauth:cookie-get'))
        self.assertContains(response, "Cookie value")


class   FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse('myauth:foo-bar'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers['content-type'], 'application/json'
        )
        expect = {'foo': 'bar'}
        ressiv = json.loads(response.content)
        self.assertEqual(ressiv, expect)

        # self.assertTemplateUsed(response,'myauth/foo_bar.html')