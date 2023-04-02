from django import forms
from django.contrib import admin

from culinary.models import Receipt, ReceiptComment, ReceiptComponent


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
        widgets = {'author': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.author:
            self.fields['author'].initial = self.request.user


class ComponentsInline(admin.TabularInline):
    model = ReceiptComponent
    extra = 1


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    inlines = [ComponentsInline]
    exclude = ('author',)


@admin.register(ReceiptComponent)
class ReceiptComponent(admin.ModelAdmin):
    pass


@admin.register(ReceiptComment)
class ReceiptComment(admin.ModelAdmin):
    pass
