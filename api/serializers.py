# system/api/serializers.py
from rest_framework import serializers
from .models import Product, Sale, SaleItem


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SaleItemSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    product_name = serializers.CharField(source="product.name", read_only=True)
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    def create(self, validated_data):
        return SaleItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SaleSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    items = SaleItemSerializer(many=True, read_only=True)
    create_items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
        ),
        write_only=True,
    )

    def create(self, validated_data):
        create_items_data = validated_data.pop("create_items", [])
        sale = Sale.objects.create(**validated_data)
        for item_data in create_items_data:
            product = Product.objects.get(id=item_data["product_id"])
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=item_data["quantity"],
                unit_price=product.price,
            )
        return sale

    def update(self, instance, validated_data):
        # Atualização da venda (se necessário)
        # Por exemplo, não atualizamos itens aqui, pois são read_only
        return instance
