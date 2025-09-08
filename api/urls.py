from django.urls import path
from .views import ProductsAPIView, SalesAPIView, ProductDetailAPIView


urlpatterns = [
    path("v1/products/", ProductsAPIView.as_view(), name="products"),
    path(
        "v1/products/<uuid:pk>/", ProductDetailAPIView.as_view(), name="product-detail"
    ),
    path("v1/sales/", SalesAPIView.as_view(), name="sales"),
]
