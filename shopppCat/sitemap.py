from django.contrib.sitemaps import Sitemap
from .models import Product,Order

class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at



    def location(self, obj):
        return obj.get_absolute_url()

