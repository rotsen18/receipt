from django.db.models import F, Func

from culinary.models import Receipt, ReceiptComponent


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
