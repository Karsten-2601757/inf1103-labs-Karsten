from product import Product


class Inventory:

    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        """A copy of the product list (typed on the Product abstraction, so
        any current or future Product subclass fits)."""
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().upper() == product_id.strip().upper():
                return product
        return None

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        if not self.__products:
            print("No products available.\n")
            return
        for product in self.__products:
            product.display_information()
        print()

    def to_list(self) -> list[dict]:
        return [product.to_dict() for product in self.__products]