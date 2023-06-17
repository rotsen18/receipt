from django.contrib import admin

from directory.models import CookingType, CulinaryCategory, Device, Ingredient, MeasurementUnit


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'default_measurement_unit', 'product_url')


@admin.register(CulinaryCategory)
class CulinaryCategoryAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['parent'].required = False
        return form


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(CookingType)
class CookingTypeAdmin(admin.ModelAdmin):
    pass
