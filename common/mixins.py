# common/mixins.py

class RoleBasedMixin:
    """
    Reusable mixin for any view that needs role based serializers.

    How to use:
        1. Add RoleBasedMixin to your view
        2. Define serializer_map in your view
        3. Call self.get_role(request) and self.get_serializer_class(request)

    Example:
        class ProductListView(RoleBasedMixin, APIView):
            serializer_map = {
                "admin":    AdminProductSerializer,
                "merchant": MerchantProductSerializer,
                "public":   PublicProductSerializer,
            }
    """

    serializer_map = {}

    def get_role(self, request):
        # no token → public
        if not request.user or not request.user.is_authenticated:
            return "public"

        # has token → check role
        if request.user.is_super_admin:
            return "admin"

        if request.user.is_merchant:
            return "merchant"

        return "public"

    def get_serializer_class(self, request):
        role = self.get_role(request)
        # fallback to public if role not in map
        return self.serializer_map.get(role, self.serializer_map.get("public"))