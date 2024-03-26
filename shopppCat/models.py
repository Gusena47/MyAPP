
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

class Product (models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


    name = models.CharField(max_length=100)
    discription = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    createt_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    arhivate = models.BooleanField(default=False)

    @property
    def descrip_short(self)-> str:
        if len(self.description)<48:
            return self.description
        return self.description[:48] + '...'

    def __str__(self)->str:
        return f"Product(pk={self.pk}, name={self.name!r}"

    def get_absolute_url(self):
        return reverse('shopppCat:product_det',kwargs={'pk': self.pk})

class Order (models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    delivery_address = models.TextField(blank=True, null=True,)
    promo_code = models.CharField(max_length=100, null=True,blank=True)
    createt_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
    # receipt = models.FileField(null=True, upload_to='orders/receipt')