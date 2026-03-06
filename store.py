"""
A module for managing a store's inventory and processing customer orders.

This module provides the `Store` class, which represents a retail store with an inventory
of `Product` objects. It supports adding/removing products, querying stock levels, and
processing purchase orders with error handling for missing or out-of-stock items.

Dependencies:
-------------
- Requires the `products` module (specifically the `Product` class).

Classes:
--------
    Store:
        A class to represent a store with inventory and order processing capabilities.

        Attributes:
            inventory (list[products.Product]): List of products available in the store.

        Methods:
            add_product(product): Adds a product to the inventory.
            remove_product(product): Removes a product from the inventory.
            get_total_quantity(): Returns the sum of all product quantities.
            get_all_products(): Returns a list of all products in the inventory.
            order(shopping_list): Processes a purchase order and returns the total price.

        Raises:
            ValueError: If a product to be removed is not found in the inventory.
"""
import products


class Store:
    """
    Represents a store that holds an inventory of products.
    """


    def __init__(self, product_list: list[products.Product]):
        """
        Initializes the store with a list of products.
        """
        self.inventory = product_list


    def add_product(self, product) -> None:
        """
        Adds a single product to the store's inventory.
        """
        self.inventory.append(product)


    def remove_product(self, product) -> None:
        """
        Removes a product from the inventory.

        Raises:
            ValueError: If the product is not found in the store's inventory.
        """
        if product not in self.inventory:
            raise ValueError(f"Product '{product.name}' not found in inventory.")
        self.inventory.remove(product)


    def get_total_quantity(self) -> int:
        """
        Returns the combined quantity of all products in stock.
        """
        return sum(p.quantity for p in self.inventory)


    def get_all_products(self) -> list[products.Product]:
        """
        Returns a list of all active products currently in the inventory.
        """
        return [product for product in self.inventory if product.is_active()]



    def order(self, shopping_list: list[tuple[products.Product, int]]) -> float:
        """
        Processes a purchase order for a list of products.

        Checks if each product is part of the store's inventory and has
        sufficient stock. If a product is missing or an error occurs
        during purchase, it is skipped and an error message is printed.

        Args:
            shopping_list: A list of tuples, where each tuple contains
                           a Product object and the quantity (int) to buy.

        Returns:
            float: The total price of all successfully processed items.
        """
        total_price = 0.0
        for product, amount in shopping_list:
            if product not in self.inventory:
                print(f"Error: {product.name} is not carried by this store.")
                continue

            try:
                total_price += product.buy(amount)
            except ValueError as error:
                print(f"Error processing order for {product.name}: {error}")
        return total_price


def main():
    """
    Test basic functionality of the Store and Product functionality.
    """
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    ]

    best_buy = Store(product_list)
    _products = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(_products[0], 1), (_products[1], 2)]))


if __name__ == '__main__':
    main()
