"""
A module for managing product entities in an inventory system.

This module provides the `Product` class, which represents a product with attributes
such as name, price, quantity, and active status. It includes methods for managing
inventory, purchasing products, and checking product availability.

Classes:
--------
    Product:
        A class to represent a product in an inventory system.

        Attributes:
            name (str): Name of the product.
            price (float): Price per unit.
            quantity (int): Available stock quantity.
            active (bool): Whether the product is available for purchase.

        Methods:
            get_quantity(): Returns current stock quantity.
            set_quantity(quantity): Updates stock and adjusts active status.
            is_active(): Returns active status.
            activate(): Sets product to active.
            deactivate(): Sets product to inactive.
            show(): Prints product details.
            buy(quantity): Processes a purchase and returns total price.
"""


class Product:
    """
    A class representing a product in the store.

    Attributes:
        name (str): The name of the product.
        price (float): The unit price of the product.
        quantity (int): The current stock level.
        active (bool): Status indicating if the product is available for sale.
    """


    def __init__(self, name: str, price: float | int, quantity: int):
        """
        Initializes a new Product instance with strict type and value validation.

        Args:
            name (str): The name of the product. Must not be empty.
            price (float): The unit price. Must be a non-negative number.
            quantity (int): The amount of stock available. Must be a non-negative integer.

        Raises:
            TypeError: If 'price' is not a number or 'quantity' is not an integer.
            ValueError: If 'name' is empty, or if 'price' or 'quantity' are negative.
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
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = self.quantity > 0


    def get_quantity(self) -> int:
        """
        Returns the current stock quantity of the product.
        """
        return self.quantity


    def set_quantity(self, quantity):
        """
        Updates the stock quantity.
        Deactivates the product if quantity reaches zero.
        """
        self.quantity = quantity
        if self.quantity <= 0:
            self.quantity = 0
            self.deactivate()


    def is_active(self) -> bool:
        """
        Returns True if the product is currently active.
        """
        return self.active


    def activate(self):
        """
        Sets the product status to active.
        Raises:
            ValueError: If quantity is 0 or less, preventing activation of empty stock.
        """
        if self.quantity < 0:
            raise ValueError(f"Cannot activate '{self.name}': Quantity is {self.quantity}.")
        self.active = True


    def deactivate(self):
        """
        Sets the product status to inactive.
        """
        self.active = False


    def show(self):
        """
        Prints a string representation of the product's current state.
        """
        print(f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}")


    def buy(self, quantity: int) -> float:
        """
        Processes a purchase of the specified quantity.

        Returns:
            float: The total price of the purchase.

        Raises:
            ValueError: If quantity is not positive or exceeds stock.
        """
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if quantity > self.quantity:
            raise ValueError("Not enough stock available.")

        new_quantity = self.get_quantity() - quantity
        self.set_quantity(new_quantity)
        return float(self.price * quantity)


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float | int):
        super().__init__(name, price, 0)

    def get_quantity(self) -> int:
        return 0

    def set_quantity(self, quantity):
        print("Quantity can not be changed for non-stock products")

    def show(self):
        print(f"{self.name}, Price: ${self.price}")

    def buy(self, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        return float(self.price * quantity)



class LimitedProduct(Product):
    def __init__(self, name: str, price: float | int, quantity: int, order_limit: int):
        super().__init__(name, price, quantity)
        self.maximum = order_limit

    def show(self):
        print(f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Order Limit: {self.maximum}")

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"Quantity exceeds the order limit of {self.maximum}")
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

    bose.set_quantity(1000)
    bose.show()


if __name__ == '__main__':
    main()
