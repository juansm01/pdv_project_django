from django.db import models
import uuid


# o objetivo da model e fazer a ponte com o banco de dados
# Esta classe representa a estrutura de um produto
class Product(models.Model):
    # objetos UUID importando do .models e do uuid(classe dentro do init)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#
class Sale(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        return f"R$ {total:.2f}"

    get_total_price.short_description = "Valor Total"

    def __str__(self):
        return f"Sale #{self.id} on {self.date.strftime('%Y-%m-%d %H:%M')}"


class SaleItem(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(Sale, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"ItemVenda: {self.product.name} (x{self.quantity})"
