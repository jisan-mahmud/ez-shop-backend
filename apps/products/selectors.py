from .models import Product
from common.exceptions import NotFoundException


class ProductSelector:

    def __init__(self, user):
        self.user = user

    def get_for_role(self, role):
        if role == "admin":
            # admin sees all products from all merchants
            return Product.objects.all().select_related("merchant")

        if role == "merchant":
            # merchant sees only their own products
            return Product.objects.filter(
                merchant=self.user
            )

        # public sees only active products
        return Product.objects.filter(is_active=True)

    def get_by_id_for_role(self, product_id, role):
        try:
            return self.get_for_role(role).get(id=product_id)
        except Product.DoesNotExist:
            raise NotFoundException("Product not found")