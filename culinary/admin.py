from django.contrib import admin

from culinary.models import (
    Receipt, ReceiptComponent, ReceiptComment,

)


class ComponentsInline(admin.TabularInline):
    model = ReceiptComponent


class CommentsInline(admin.TabularInline):
    model = ReceiptComment


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    inlines = [ComponentsInline, CommentsInline]
