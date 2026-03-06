"""
Abstract base class and concrete implementations for product promotion strategies.

This module defines an abstract base class `Promotion` that serves as an interface for
various product discount strategies. It includes concrete implementations for common
promotion types such as "Second Half Price", "Third One Free", and "Percentage Discount".

The module follows the Strategy Pattern, allowing flexible interchange of promotion
algorithms at runtime. All promotion classes validate input parameters and maintain
consistent behavior through property getters/setters with strict validation.

Classes:
--------
    Promotion (ABC):
        Abstract base class defining the promotion interface.
        Requires implementation of `apply_promotion(product, quantity)`.

        Properties:
            name (str): Human-readable promotion name.
            discount_percent (int): Base discount percentage (0-100).

        Methods:
            apply_promotion(product, quantity): Abstract method to calculate discounted price.

    SecondHalfPrice(Promotion):
        Every second item is sold at 50% off.
        Example: Buy 3 items → pay for 2.5 items.

    ThirdOneFree(Promotion):
        Every third item is free.
        Example: Buy 3 items → pay for 2 items.

    PercentDiscount(Promotion):
        Applies a percentage discount to the total price.
        Example: 20% off → pay 80% of the original price.

"""
from abc import ABC, abstractmethod

class Promotion(ABC):
    """
    Abstract base class for all product promotions.

    This class defines the interface for applying discounts to products.
    Subclasses must implement the 'apply_promotion' method.

    Attributes:
        name (str): The descriptive name of the promotion.
        discount_percent (int): The percentage of the discount (0-100).
    """
    def __init__(self, name: str, discount_percent: int =0):
        """
        Initializes a promotion with a name and an optional discount percentage.

        Args:
            name (str): The name of the promotion. Must be a non-empty string.
            discount_percent (int): Discount in percent. Defaults to 0.

        Raises:
            ValueError: If name is empty or discount_percent is out of range (0-100).
            TypeError: If types of arguments are incorrect.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(discount_percent, int):
            raise TypeError("Discount percent must be an integer")
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount percent must be between 0 and 100")
        self.__name = name
        self.__discount_percent = discount_percent

    @property
    def name(self) -> str:
        """Returns the name of the promotion."""
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Updates the promotion name with validation.

        Args:
            name (str): The new name. Must be a non-empty string.

        Raises:
            ValueError: If the name is empty or only whitespace.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        self.__name = name

    @property
    def discount_percent(self) -> float | int:
        """Returns the discount percentage."""
        return self.__discount_percent

    @discount_percent.setter
    def discount_percent(self, discount_percent: int):
        """
        Updates the discount percentage with strict validation.

        Args:
            discount_percent (int): The new percentage (0-100).

        Raises:
            TypeError: If the input is not an integer.
            ValueError: If the value is not between 0 and 100.
        """
        if not isinstance(discount_percent, int):
            raise TypeError("Discount percent must be an integer")
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount percent must be between 0 and 100")
        self.__discount_percent = discount_percent

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Calculates the price for a product quantity after applying the promotion.

        Args:
            product (Product): The product to apply the promotion to.
            quantity (int): Number of items.

        Returns:
            float: Total price after discount.
        """


class SecondHalfPrice(Promotion):
    """
    Promotion: Every second item of the same product is half price.
    Example: Buy 2, pay 1.5 times the price. Buy 4, pay 3 times the price.
    """
    def apply_promotion(self, product, quantity) -> float| int:
        """
        Calculates the price where every second item costs 50% less.

        Args:
            product (Product): The product to apply the discount to.
            quantity (int): Number of items.

        Returns:
            float: The total price after applying the 'Buy 1, get 2nd half price' rule.
        """
        half_price_items = quantity // 2
        full_price_items = quantity - half_price_items
        return (full_price_items * product.price) + (half_price_items * product.price * 0.5)


class ThirdOneFree(Promotion):
    """
    Promotion: Buy three items of the same product, and the third one is free.
    Example: 3 for the price of 2, 6 for the price of 4, etc.
    """
    def apply_promotion(self, product, quantity) -> float | int:
        """
        Calculates the total price where every third item is free of charge.

        Args:
            product (Product): The product to apply the discount to.
            quantity (int): Number of items.

        Returns:
            float | int: Total price after removing the cost of free items.
        """
        free_items = quantity // 3
        payable_quantity = quantity - free_items
        return product.price * payable_quantity


class PercentDiscount(Promotion):
    """
    Promotion: Applies a percentage-based discount to the total price.
    Example: 10% off the total, 50% off, etc.
    """
    def apply_promotion(self, product, quantity) -> float | int:
        """
        Calculates the price with a percentage discount applied.

        Args:
            product (Product): The product to calculate the price for.
            quantity (int): The number of units being purchased.

        Returns:
            float | int: Total price minus the percentage discount.
        """
        total = product.price * quantity
        discount = total * (self.discount_percent / 100)
        return total - discount
