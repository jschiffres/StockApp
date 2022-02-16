from django.contrib import admin
from .models import Stock, Portfolio, Transaction, TransactionTwo, Holding

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields=('buyvalue',)

admin.site.register([Stock, Portfolio, Transaction, TransactionTwo, Holding])