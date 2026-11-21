from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total
    
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage
    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)
    
class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount
    def apply(self, total: float) -> float:
        return total - self.__amount if total >= self.__threshold else total
    
class StudentDiscount(DiscountStrategy):
    """Fourth strategy: 5% off. Added without changing Order at all."""
    def apply(self, total: float) -> float:
        return total * 0.95