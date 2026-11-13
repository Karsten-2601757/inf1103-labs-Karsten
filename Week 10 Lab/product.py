from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if price < 0 or stock < 0:
            raise ValueError("Stock value and price cannot be negative.")
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        # Association: Product only holds a reference to an independent Supplier.
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> bool:
        if not isinstance(quantity, int) or quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        print(f"    Supplied by: {self.__supplier.get_name()} "
              f"({self.__supplier.get_contact_email()})")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Each product type must say how it is fulfilled."""
        pass

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }