from django.core.management.base import BaseCommand

from culinary.services import UpgradeProduct


class Command(BaseCommand):

    def handle(self, *args, **options):
        UpgradeProduct.update_all_products_data()
        return
