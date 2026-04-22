from rest_framework import serializers
from .models import Product


# public sees minimum
class PublicProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ["id", "name", "price", "image", "description"]


# merchant sees own product details
class MerchantProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ["id", "name", "price", "image", "description",
                  "stock", "is_active", "created_at"]


# admin sees everything including who owns it
class AdminProductSerializer(serializers.ModelSerializer):
    merchant_email = serializers.EmailField(source="merchant.email", read_only=True)

    class Meta:
        model  = Product
        fields = ["id", "name", "price", "image", "description",
                  "stock", "is_active", "merchant_email", "created_at", "updated_at"]


# input — for creating product
class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    stock = serializers.IntegerField(default=0)