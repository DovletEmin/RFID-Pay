import uuid
from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rf_id = models.CharField(max_length=100)
    balance = models.FloatField()
    img = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'client'
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        ordering = ['-created_at']
        
        

class Point(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    balance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.id}'
    
    
    class Meta:
        db_table = 'point'
        verbose_name = 'point'
        verbose_name_plural = 'points'
        ordering = ['-created_at']
        
        
        
class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.client} ==> {self.point}'
    
    
    class Meta:
        db_table = 'payment'
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
        
        