from django.contrib import admin
from .models import CarModel, Client, Car,Services, ServicesRows, Order

class ServicesOrdersInline(admin.TabularInline):
    model = ServicesRows

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'display_service_rows_quant', 'display_services', 'display_service_rows_prices', )
    list_editable = ('date', )
    inlines = [ServicesOrdersInline]

    def total_price_for_user(self, obj):
        # Calculate the total price for the user by summing the prices of related services
        total_price = sum(row.price for row in obj.orders.all())
        return total_price

    total_price_for_user.short_description = "Total Price"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    search_fields = ('i_nr', 'vin', )
    list_display = ('client', 'car_mod', 'vin', 'i_nr', )
    list_filter = ('client', 'car_mod', )


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(ServicesRows)
class ServiceRowsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {'fields': ('id', 'car')}),
        ('Details', {'fields': ('quantity', 'price')}),
    )


admin.site.register(CarModel)
admin.site.register(Client)


# Register your models here.
