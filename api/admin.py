# Register your models here

from django.contrib import admin
from .models import Product, Sale, SaleItem


class SaleItemInline(admin.TabularInline):

    model = SaleItem
    fields = ["product", "quantity", "unit_price"]
    #readonly_fields = ["unit_price"]
    extra = 0


class SaleAdmin(admin.ModelAdmin):

    list_display = ("id", "date", "get_total_price")
    list_filter = ("date",)
    inlines = [SaleItemInline]
    readonly_fields = ("date", "get_total_price")

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = "Valor Total"


class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "price", "stock", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
