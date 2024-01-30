from django.contrib import admin
# from .models import related models
from .models import CarMake,CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1
# CarModelAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    fields = ["name","description","brand"]
    inlines = [CarModelInline]
# CarMakeAdmin class with CarModelInline
class CarModelAdmin(admin.ModelAdmin):
    fields = ["name", "dealer_id", "year", "type", "car_make",]
# Register models here
admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel,CarModelAdmin)