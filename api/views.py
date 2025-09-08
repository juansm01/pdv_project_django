# view do projeto


# import api view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# cada models representa uma tabela no banco de dados, estrutura
from .models import Product, Sale, SaleItem
from .serializers import ProductSerializer, SaleSerializer
from api.utils.logger import logger
from rest_framework.exceptions import ValidationError

# classe para listar todos os produtos e cadastrar um novo produto
class ProductsAPIView(APIView):

    # api para listar todos produtos
    def get(self, request):
        products = Product.objects.all()
        logger.info(f"Listando todos os produtos{products}")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Api para cadastrar um novo produto
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# classe para listar todas as vendas e cadastrar uma nova venda
class SalesAPIView(APIView):

    # Listar venda
    def get(self, request):
        sales = Sale.objects.prefetch_related("items__product").all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Registrar uma nova venda
    def post(self, request):
        logger.info(f"Listando todos os produtos{request.data}")
        from api.controller.sale.create import create

        # conteudo da request (body)
        return create(request.data)

# classe para detalhar, atualizar e deletar um produto
class ProductDetailAPIView(APIView):

    # Listar produto
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # Atualizar produto todo com o campo
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletar produto
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # logger de uma nova venda
    def perform_create(self, serializer):
        try:
            serializer.save()
            logger.info("Venda registrada com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao registrar a venda: {e}")
            raise
