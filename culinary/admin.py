from django.contrib import admin

from culinary.models import (
    Receipt, ReceiptComponent, ReceiptComment,

)


class ComponentsInline(admin.TabularInline):
    model = ReceiptComponent


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    inlines = [ComponentsInline]


@admin.register(ReceiptComponent)
class ReceiptComponent(admin.ModelAdmin):
    pass


@admin.register(ReceiptComment)
class ReceiptComment(admin.ModelAdmin):
    pass
