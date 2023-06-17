from django.core.management.base import BaseCommand

from culinary.services import ReceiptPriceService
from directory.models import Ingredient


class Command(BaseCommand):
    help = 'Update products data'

    def handle(self, *args, **options):
        bulk_ingredients = []
        for ingredient in Ingredient.objects.all():
            try:
                data = ReceiptPriceService.get_product_info(ingredient)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'{ingredient}: status Error: {e}'))
                continue
            self.stdout.write(self.style.SUCCESS(f'{ingredient}: status OK'))
            ingredient.product_data = data
            bulk_ingredients.append(ingredient)
        Ingredient.objects.bulk_update(bulk_ingredients, ['product_data'])
        self.stdout.write(self.style.SUCCESS('All data updated successfully'))
        return
