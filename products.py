"""
A module for managing product entities in an inventory system with promotion support.

This module provides a hierarchy of product classes for different inventory scenarios:
- `Product`: Standard physical products with stock management.
- `NonStockedProduct`: Digital/non-physical products without inventory tracking.
- `LimitedProduct`: Physical products with per-order purchase quantity limits.

All product types support promotional pricing through the `Promotion` interface,
allowing flexible discount strategies (e.g., percentage discounts, "buy X get Y" offers).

Class Hierarchy:
----------------
    Product (Base):
        Core product with stock tracking and promotion support.

        Attributes:
            self.name (str): Product name (read-only).
            self.price (float): Unit price with validation.
            self.quantity (int): Current stock level (auto-managed).
            self.active (bool): Availability status (auto-updated).
            self.promotion (Promotion): Associated discount strategy.

        Methods:
            buy(quantity): Processes purchases with promotion application.
            show(): Displays product details.

    NonStockedProduct (Product):
        Represents products without physical inventory (e.g., software licenses).
        Overrides quantity management to always return 0.

    LimitedProduct (Product):
        Extends Product with per-order quantity limits.
        Validates purchase quantities against the defined limit.
"""

from promotions import Promotion

class Product:
    """
    Represents a standard product in the store with stock tracking.

    Attributes:
        __name (str): The name of the product.
        __price (float | int): The unit price.
        __quantity (int): Current stock level.
        __active (bool): Whether the product is available for purchase.
        __promotion (Promotion | None): Associated discount logic.
    """


    def __init__(self, name: str, price: float | int, quantity: int):
        """
        Initializes a new Product instance.

        Args:
            name (str): Name of the product (non-empty).
            price (float | int): Price per unit (non-negative).
            quantity (int): Initial stock (non-negative).

        Raises:
            TypeError: If price is not numeric or quantity is not an integer.
            ValueError: If name is empty or values are negative.
        """
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number (int or float)")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")

        if not name:
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.__promotion: Promotion | None = None
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__active = self.quantity > 0

    @property
    def quantity(self) -> int:
        """Returns the current stock quantity."""
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity):
        """ Updates stock and automatically deactivates product if quantity hits zero."""
        self.__quantity = quantity
        if self.quantity <= 0:
            self.__quantity = 0
            self.deactivate()

    def is_active(self) -> bool:
        """Checks if the product is currently available for sale."""
        return self.__active

    def activate(self):
        """
        Sets the product status to active.
        Raises:
            ValueError: If quantity is 0 or less, preventing activation of empty stock.
        """
        if self.quantity <= 0:
            raise ValueError(f"Cannot activate '{self.name}': Quantity is {self.quantity}.")
        self.__active = True

    def deactivate(self):
        """ Sets the product status to inactive. """
        self.__active = False

    def show(self):
        """ Prints a string representation of the product's current state. """
        print(f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}")

    def buy(self, quantity: int) -> float | int:
        """
        Processes a purchase and updates inventory.

        Args:
            quantity (int): Amount to buy.

        Returns:
            float: Total cost after applying promotions (if any).

        Raises:
            ValueError: If quantity is non-positive or exceeds stock.
        """
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if quantity > self.quantity:
            raise ValueError("Not enough stock available.")

        new_quantity = self.quantity - quantity
        self.quantity = new_quantity
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return float(self.price * quantity)

    @property
    def name(self) -> str:
        """The name of the product (Read-only)."""
        return self.__name

    @property
    def price(self) -> float | int:
        """The unit price of the product."""
        return self.__price

    @price.setter
    def price(self, value: float):
        """Updates price with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number (int or float)")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value

    @property
    def promotion(self) -> Promotion:
        """The promotion currently applied to this product."""
        return self.__promotion

    @promotion.setter
    def promotion(self, promotion: Promotion):
        """Sets a new promotion for the product."""
        if not isinstance(promotion, Promotion):
            raise TypeError("Promotion must be a Type Promotion")
        self.__promotion = promotion


class NonStockedProduct(Product):
    """
    A product type that represents items without physical stock (e.g., digital software).

    This class overrides quantity management to ensure that the product is
    always available for purchase without depleting an inventory.
    """
    def __init__(self, name: str, price: float | int):
        """Initializes a non-stocked product with a fixed quantity of 0."""
        super().__init__(name, price, 0)

    @property
    def quantity(self) -> int:
        """Always returns 0, as these products do not have a physical inventory."""
        return 0

    @quantity.setter
    def quantity(self, _quantity):
        """Prevents changing the quantity, as it is irrelevant for non-stocked items."""
        print("Quantity can not be changed for non-stock products")

    def show(self):
        """Displays product details without showing a quantity."""
        print(f"{self.name}, Price: ${self.price}")

    def buy(self, quantity: int) -> float | int:
        """
        Processes a purchase without checking or deducting stock levels.

        Args:
            quantity (int): The number of items to buy.

        Returns:
            float | int: Total price, applying promotions if available.
        """
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return float(self.price * quantity)


class LimitedProduct(Product):
    """
    A product type that limits the amount a customer can buy in a single order.

    Useful for promotional items or products with restricted availability.
    """
    def __init__(self, name: str, price: float | int, quantity: int, order_limit: int):
        """
        Initializes a limited product with an additional order restriction.

        Args:
            order_limit (int): Maximum units allowed per single purchase.
        """
        super().__init__(name, price, quantity)
        self.__order_limit = order_limit

    @property
    def order_limit(self):
        """Returns the maximum allowed quantity per order."""
        return self.__order_limit

    def show(self):
        """Displays product details including the specific order limit."""
        print(f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, "
              f"Order Limit: {self.order_limit}")

    def buy(self, quantity: int) -> float | int:
        """
        Processes a purchase after verifying the order limit.

        Args:
            quantity (int): The number of items to buy.

        Raises:
            ValueError: If quantity exceeds the defined order_limit.

        Returns:
            float | int: Total price calculated by the base class logic.
        """
        if quantity > self.order_limit:
            raise ValueError(f"Quantity exceeds the order limit of {self.order_limit}")
        return super().buy(quantity)



def main():
    """
    Test basic functionality of the Product class.
    """
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.quantity = 1000
    bose.show()


if __name__ == '__main__':
    main()
