from rest_framework.generics import CreateAPIView ,ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from common.mixins import RoleBasedMixin
from common.permissions import IsMerchant

from .serializers import (
    PublicProductSerializer,
    MerchantProductSerializer,
    AdminProductSerializer,
    CreateProductSerializer
)
from .services import (
    CreateProductService,
)
from .selectors import ProductSelector
from .paginations import ProductPagination


class MerchantProductCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = CreateProductSerializer

    def perform_create(self, serializer):
        CreateProductService.run(
            merchant=self.request.user,
            **serializer.validated_data,
        )
    
    @extend_schema(
        tags=["Products — Merchant"],
        summary="Create product — Merchant only",
        request=CreateProductSerializer,
        responses={
            201: MerchantProductSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Not a merchant"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProductListView(RoleBasedMixin, ListAPIView):
    """ Role-based view → list of products. """
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]
    pagination_class = ProductPagination
    
    serializer_map = {
        'admin': AdminProductSerializer,
        'merchant': MerchantProductSerializer,
        'public': PublicProductSerializer
    }

    @extend_schema(
        tags=["Products"],
        summary="List active products",
    )
    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return ProductSelector(user=self.request.user).list_for_role(role=self.get_role(self.request))


class ProductDetailView(RoleBasedMixin, RetrieveAPIView):
    """ Role-based view → single product detail."""
    permission_classes = [AllowAny]
    lookup_field  = "pk"
    lookup_url_kwarg = "product_id"
    serializer_map = {
        'admin': AdminProductSerializer,
        'merchant': MerchantProductSerializer,
        'public': PublicProductSerializer
    }

    def get_object(self):
        return ProductSelector(user=self.request.user).get_by_id(
            product_id= self.kwargs["product_id"]
        )
        
    @extend_schema(
        tags=["Products"],
        summary="Get product detail",
    )
    @method_decorator(cache_page(60 * 10, key_prefix= 'product_details'))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)