# apps/products/services.py
from django.utils.text import slugify
from common.services import BaseService
from common.exceptions import ServiceException
from .models import Product


class CreateProductService(BaseService):

    def __init__(self, merchant, name, price, description="", stock=0, category=None):
        self.merchant = merchant
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.category = category

    def execute(self):
        self.__validate()
        return Product.objects.create(
            merchant=self.merchant,
            name=self.name,
            slug=self._generate_slug(),    # auto generate
            price=self.price,
            description=self.description,
            stock=self.stock,
            category=self.category,
            status=Product.Status.ACTIVE,
        )

    def _generate_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        # if slug exists add number → iphone-15, iphone-15-1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    
    def __validate(self):
        if self.stock < 0:
            raise ServiceException(
                detail="Stock cannot be negative"
            )

        if self.price < 0:
            raise ServiceException(
                detail="Price cannot be negative"
            ) 
    
    @classmethod
    def run(cls, **kwargs):
        return cls(**kwargs).execute()