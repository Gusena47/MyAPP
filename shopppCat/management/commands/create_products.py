from django.core.management.base import BaseCommand
from shopppCat.models import Product
class Command(BaseCommand):
    # create products

    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products_name = [
            'Laptop',
            'Desktop',
            'Smartphone',
        ]

        for product_name in products_name:
            product,create = Product.objects.get_or_create(name=product_name)
            self.stdout.write(self.style.SUCCESS(f'{product_name} created'))

        self.stdout.write(self.style.SUCCESS('Creating products'))