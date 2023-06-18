import asyncio
from collections import defaultdict

import httpx
from django.conf import settings
from django.db.models import F, Func

from culinary.models import Receipt, ReceiptComponent
from directory.models import Ingredient


class PortionService:
    @staticmethod
    def new_portions(receipt: Receipt | int, portions: int):
        if isinstance(receipt, int):
            receipt = Receipt.objects.get(id=receipt)
        qs = ReceiptComponent.objects.filter(receipt=receipt).select_related('ingredient', 'measurement_unit').annotate(
            ingredient_name=F('ingredient__name'),
            measurement_unit_name=F('measurement_unit__name'),
            new_amount=Func(
                (F('amount') * portions) / F('receipt__receipt_portions'),
                function='ROUND',
                template='%(function)s(%(expressions)s::numeric, 1)'
            )
        ).values('ingredient_name', 'measurement_unit_name', 'new_amount')
        return list(qs)


class ReceiptPriceService:
    def __init__(self, receipt: Receipt):
        self.receipt = receipt
        self.receipt_price = None
        self.profit_cost = None
        self.consumption_cost = None
        self.products_cost = None
        self._components_price = defaultdict(float)
        self.calculate()

    @staticmethod
    def get_component_price(component: ReceiptComponent) -> float:
        ingredient_unit = component.measurement_unit or component.ingredient.default_measurement_unit
        product_info = component.ingredient.product_data
        if not product_info:
            return 0
        product_price = product_info['price'] * 0.01
        product_unit_name = product_info['unit']
        if ingredient_unit.name == 'грам':
            if product_unit_name == 'pcs':
                return product_price / product_info['weight']
            elif product_unit_name == 'kg':
                return product_price / 1000
        elif ingredient_unit.name == 'кілограм':
            if product_unit_name == 'pcs':
                return product_price / product_info['weight'] * 1000
            elif product_unit_name == 'kg':
                return product_price
        elif ingredient_unit.name == 'столова ложка':
            if product_unit_name == 'pcs':
                price = product_price / product_info['weight']
                return price * 12
            elif product_unit_name == 'kg':
                price = product_price / 1000
                return price * 12
        elif ingredient_unit.name == 'чайна ложка':
            if product_unit_name == 'pcs':
                price = product_price / product_info['weight']
                return price * 5
            elif product_unit_name == 'kg':
                price = product_price / 1000
                return price * 5
        elif ingredient_unit.name == 'щіпка':
            if product_unit_name == 'pcs':
                return product_price / product_info['weight']
            elif product_unit_name == 'kg':
                return product_price / 1000
        elif ingredient_unit.name == 'штук':
            if product_unit_name == 'pcs':
                return product_price / product_info['pack_amount']

    def calculate(self):
        products_cost = 0
        for component in self.receipt.components.all():
            product_amount = component.amount * self.get_component_price(component=component)
            self._components_price[component.ingredient.name] += product_amount
            products_cost += product_amount
        self.products_cost = round(products_cost, 2)

        electricity_cost = self.receipt.estimate_time.total_seconds() / 3600 * settings.ELECTRICITY_PRICE
        water_sewer_cost = settings.WATER_SEWER_PRICE * 0.015
        self.consumption_cost = round(electricity_cost + water_sewer_cost, 2)
        receipt_cost = self.products_cost + self.consumption_cost
        self.profit_cost = round(settings.PROFIT_PERCENT * receipt_cost, 2)
        self.receipt_price = round(receipt_cost + self.profit_cost, 2)

    def get_components_price_text(self) -> list:
        return [
            f'{index}: {ingredient[0]} - {ingredient[1]:.2f} грн'
            for index, ingredient in enumerate(self._components_price.items(), 1)
        ]


class UpgradeProduct:
    @staticmethod
    async def get_product_info(client, ingredient: Ingredient) -> Ingredient | None:
        if not ingredient.product_url:
            print(f'{ingredient}: no product_url')
            return
        product_url = ingredient.product_url.strip('/')
        product_ean = product_url.split('--')[-1]
        url = f'https://stores-api.zakaz.ua/stores/{settings.HOME_STORE_ID}/products/{product_ean}/'
        response = await client.get(url)
        new_data = response.json()
        old_price = round(ingredient.product_data.get('price') / 100, 2)
        new_price = round(new_data.get('price') / 100, 2)
        print(f'{ingredient}: {"{:.2f}".format(old_price)} UAH -> {"{:.2f}".format(new_price)} UAH')
        ingredient.product_data = new_data
        return ingredient

    @classmethod
    async def get_all_components_info(cls) -> list[dict]:
        async with httpx.AsyncClient() as client:
            tasks = []
            async for ingredient in Ingredient.objects.all():
                tasks.append(asyncio.ensure_future(cls.get_product_info(client, ingredient)))
            result = await asyncio.gather(*tasks)
            ingredients_to_update = [ingredient for ingredient in result if ingredient]
            print('All data received')
            return ingredients_to_update

    @classmethod
    def update_all_products_data(cls):
        updated_data = asyncio.run(cls.get_all_components_info())
        Ingredient.objects.bulk_update(updated_data, ['product_data'])
        print('All data updated successfully')
        return True
