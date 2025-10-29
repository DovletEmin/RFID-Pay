from django.contrib import admin
from . import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'rf_id', 'balance', 'created_at', 'updated_at',)
    
@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'balance',)
    
    
@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'point', 'balance',)