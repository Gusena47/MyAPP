from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from shopppCat.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Create order')
        user = User.objects.get(username='Admin1')
        order = Order.objects.get_or_create(
            delivery_address='Pupkin str.',
            promo_code='NewYear',
            user=user,
        )

        self.stdout.write(self.style.SUCCESS(f'Creating order {order}'))