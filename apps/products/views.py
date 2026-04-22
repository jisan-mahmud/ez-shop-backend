# apps/products/views.py
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from common.mixins import RoleBasedMixin
from common.permissions import IsMerchant, IsAdmin

from .models import Product
from .serializers import (
    PublicProductSerializer,
    MerchantProductSerializer,
    AdminProductSerializer,
    CreateProductSerializer,
    UpdateProductSerializer,
)
from .selectors import ProductSelector
from .services import (
    CreateProductService,
    UpdateProductService,
    DeleteProductService,
)


class ProductListView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class   = PublicProductSerializer
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ["category"]
    search_fields      = ["name", "description"]
    ordering_fields    = ["price", "created_at"]
    ordering           = ["-created_at"]

    @extend_schema(
        tags=["Products — Public"],
        summary="List active products",
    )
    def get_queryset(self):
        return Product.objects.filter(
            status=Product.Status.ACTIVE
        ).select_related("category")


class ProductDetailView(RetrieveAPIView):
    """Public → single product detail."""
    permission_classes = [AllowAny]
    serializer_class   = PublicProductSerializer
    lookup_field       = "pk"
    lookup_url_kwarg   = "product_id"

    @extend_schema(
        tags=["Products — Public"],
        summary="Get product detail",
    )
    def get_queryset(self):
        return Product.objects.filter(
            status=Product.Status.ACTIVE
        ).select_related("category", "merchant")

class MerchantProductListView(ListAPIView):
  
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class   = MerchantProductSerializer
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ["status", "category"]
    search_fields      = ["name", "description"]
    ordering_fields    = ["price", "created_at", "stock"]
    ordering           = ["-created_at"]

    @extend_schema(
        tags=["Products — Merchant"],
        summary="List own products — Merchant only",
    )
    def get_queryset(self):
        # merchant sees only their own
        return Product.objects.filter(
            merchant=self.request.user
        ).select_related("category")


class MerchantProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsMerchant]

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
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = CreateProductService.run(
            merchant=request.user,
            **serializer.validated_data,
        )
        return Response(
            MerchantProductSerializer(product).data,
            status=status.HTTP_201_CREATED,
        )


class MerchantProductUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsMerchant]

    @extend_schema(
        tags=["Products — Merchant"],
        summary="Update own product — Merchant only",
        request=UpdateProductSerializer,
        responses={
            200: MerchantProductSerializer,
            403: OpenApiResponse(description="Not your product"),
            404: OpenApiResponse(description="Not found"),
        }
    )
    def put(self, request, product_id):
        product = ProductSelector(user=request.user).get_own_by_id(product_id)

        serializer = UpdateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = UpdateProductService.run(
            user=request.user,
            product=product,
            **serializer.validated_data,
        )
        return Response(MerchantProductSerializer(product).data)


class MerchantProductDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsMerchant]

    @extend_schema(
        tags=["Products — Merchant"],
        summary="Delete own product — Merchant only",
        responses={
            204: OpenApiResponse(description="Deleted"),
            403: OpenApiResponse(description="Not your product"),
            404: OpenApiResponse(description="Not found"),
        }
    )
    def delete(self, request, product_id):
        product = ProductSelector(user=request.user).get_own_by_id(product_id)

        DeleteProductService.run(
            user=request.user,
            product=product,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminProductListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class   = AdminProductSerializer
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ["status", "category"]
    search_fields      = ["name", "description", "merchant__email"]
    ordering_fields    = ["price", "created_at", "stock"]
    ordering           = ["-created_at"]

    @extend_schema(
        tags=["Products — Admin"],
        summary="List all products — Admin only",
    )
    def get_queryset(self):
        # admin sees everything
        return Product.objects.all().select_related("category", "merchant")
