from django.contrib import admin
from.models import Customer, TariffCategory, per_unit_price_model, Bill, Payment

admin.site.register(Customer)
admin.site.register(TariffCategory)
admin.site.register(Payment) 
admin.site.register(per_unit_price_model)
admin.site.register(Bill)