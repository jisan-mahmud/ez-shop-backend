from .models import Product
from common.exceptions import NotFoundException


class ProductSelector:

    def __init__(self, user=None):
        self.user = user

    # LIST (role-based filtering is OK)
    def list_for_role(self, role):
        if role == "admin":
            return Product.objects.all().select_related("merchant")

        if role == "merchant":
            return Product.objects.filter(
                merchant=self.user
            ).select_related("merchant")

        return Product.objects.filter(
            status=Product.Status.ACTIVE
        ).select_related("merchant")

    # DETAIL (fetch only, no role filtering)
    def get_by_id(self, product_id):
        try:
            return Product.objects.select_related("merchant").get(id=product_id)
        except Product.DoesNotExist:
            raise NotFoundException("Product not found")