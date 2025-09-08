# Em core/tests.py

from django.test import TestCase
from .models import Product, Sale, SaleItem
from decimal import Decimal
from api.utils.logger import logger

#classe de teste para o modelo Sale
class SaleTestCase(TestCase):

    def setUp(self):
        # gera um produto um produto e uma venda para usar nos testes
        self.product = Product.objects.create(name="Smartphone", price=500.00, stock=10)
        # gera um item de venda associado à venda e ao produto
        self.sale = Sale.objects.create()
        self.sale_item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=2,
            unit_price=self.product.price,
        )
        # Log de informação para indicar que o setup foi concluído
        logger.info("Setup do teste concluído: Produto e Venda criados.")
    # Testa o método get_total_price do modelo Sale
    def test_get_total_price_method(self):
        """Testa se o método get_total_price retorna o valor total correto."""
        # O valor total esperado é 2 * 500.00 = 1000.00
        expected_total = Decimal("1000.00")
        actual_total_string = self.sale.get_total_price()

        # O valor é retornado como uma string "R$ 1000.00"
        # Precisamos extrair o número para a comparação
        actual_total = Decimal(actual_total_string.replace("R$ ", ""))

        # Faz a asserção (verificação) para garantir que o resultado é o esperado
        self.assertEqual(actual_total, expected_total)

        logger.info(f"Total da venda calculado: {actual_total_string}")
