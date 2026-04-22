from django.db import transaction


class BaseService:
    """
    All services inherit from this.

    How to use:
        1. Inherit from BaseService
        2. Implement execute() method
        3. Call YourService.run(**kwargs) from view

    Example:
        class CreateProductService(BaseService):
            def __init__(self, merchant, name, price):
                self.merchant = merchant
                self.name     = name
                self.price    = price

            def execute(self):
                return Product.objects.create(
                    merchant=self.merchant,
                    name=self.name,
                    price=self.price,
                )

        # in view
        product = CreateProductService.run(
            merchant=request.user,
            name="Phone",
            price=999,
        )
    """

    def execute(self):
        raise NotImplementedError("Subclass must implement execute()")

    @classmethod
    def run(cls, **kwargs):
        """Shortcut — creates instance and calls execute() in one line."""
        return cls(**kwargs).execute()

    @classmethod
    def run_atomic(cls, **kwargs):
        """Same as run() but wrapped in a DB transaction."""
        with transaction.atomic():
            return cls(**kwargs).execute()