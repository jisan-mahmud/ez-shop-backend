from django.urls import path
from .views import (
    MerchantProductCreateView,
    ProductListView,
    ProductDetailView
)

urlpatterns = [
    path('products/create/', MerchantProductCreateView.as_view(), name='create-product'),
    path('products/', ProductListView.as_view(), name='list-products'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
]
