from rest_framework import serializers
from api.serializers import SaleSerializer
from api.utils.logger import logger
from ...models import Product, Sale, SaleItem
from rest_framework.response import Response
from rest_framework import status

# CONTROLLER


def create(validated_data):
    logger.info("Método create do SaleSerializer iniciado.")

    items_data = validated_data.pop("create_items")
    sale = Sale.objects.create(**validated_data)

    for item in items_data:
        product = item["product"]
        quantity = item["quantity"]
        try:
            product = Product.objects.get(id=product)
        except Product.DoesNotExist:
            raise ValueError(f"Produto com id {product} não encontrado")
        # lógica de estoque
        if product.stock < quantity:
            raise serializers.ValidationError(
                f"Estoque insuficiente para o produto {product.name}"
                f"disponível: {product.stock}"
            )

        product.stock -= quantity
        product.save()

        SaleItem.objects.create(
            sale=sale, product=product, quantity=quantity, unit_price=product.price
        )

        # Serializa e retorna a resposta correta
        serializer = SaleSerializer(sale)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
