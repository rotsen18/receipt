from culinary.models import Receipt


class PortionService:
    @staticmethod
    def new_portions(receipt: Receipt | int, portions: int):
        if isinstance(receipt, int):
            receipt = Receipt.objects.get(id=receipt)
        result = []
        for component in receipt.components.all():
            recalculated_data = {
                'name': component.ingredient.name,
                'measurement_unit': component.measurement_unit.name,
                'amount': round((component.amount * portions) / receipt.receipt_portions, 1)
            }
            result.append(recalculated_data)
        return result
