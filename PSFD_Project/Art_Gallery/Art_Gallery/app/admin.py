from django.contrib import admin
from .models import *



@admin.register(Art)
class ArtModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discount_price','category','art_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','pincode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','art','quantity']