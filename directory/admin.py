from django.contrib import admin

from directory.models import (
    MeasurementUnit, Ingredient, CulinaryCategory, Device, CookingType,
)


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(CulinaryCategory)
class CulinaryCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(CookingType)
class CookingTypeAdmin(admin.ModelAdmin):
    pass
