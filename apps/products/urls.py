from django.urls import path
from .views import (
    MerchantProductCreateView,
    ProductListView,
    ProductDetailView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='list-products'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', MerchantProductCreateView.as_view(), name='create-product'),
]
