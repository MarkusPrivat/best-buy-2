"""
Best Buy Store Manager – A command-line interface for managing a
retail store's inventory and orders.

This module provides a user-friendly CLI to interact with a `Store` object, enabling:
- Listing all available products.
- Displaying the total quantity of items in stock.
- Creating and processing customer orders with real-time validation.
- Graceful error handling for invalid inputs or unavailable products.

The application is built on top of the `store` and `products` modules, which define the core
business logic for inventory management and order processing.

Dependencies:
-------------
- `store`: Provides the `Store` class for inventory and order management.
- `products`: Provides the `Product` class for product representation.

Functions:
----------
    store_list_all_products(best_buy: store.Store) -> None:
        Displays all products in the store's inventory.

    store_show_total_amount(best_buy: store.Store) -> None:
        Shows the total quantity of items in stock.

    store_make_order(best_buy: store.Store) -> None:
        Guides the user through creating an order, including product
        selection and quantity input.

    get_product(best_buy: store.Store) -> products.Product | None:
        Prompts the user to select a product by its ID. Returns `None`
        if the user chooses to finish.

    get_product_quantity(product: products.Product) -> int | None:
        Prompts the user to input a quantity for the selected product.
        Returns `None` if aborted.

    exit_program(_best_buy: store.Store) -> None:
        Exits the program gracefully.

    show_menu() -> str:
        Displays the main menu and prompts the user for a choice.

    get_menu_choice() -> str:
        Validates and returns the user's menu selection.

    start(best_buy: store.Store) -> None:
        Main loop for the application, handling user input and dispatching commands.

    main() -> None:
        Initializes the store with sample products and starts the application.

Constants:
----------
    APP_NAME: The name of the application.
    MENU_LINE: A visual separator for menu formatting.
    MENU_NUM_EXIT: The menu option number for exiting the application.
    EXIT_MSG: The message displayed when exiting the application.
    MENU_DISPATCHER: A dictionary mapping menu options to their corresponding functions.
"""
import products
import store
import promotions

APP_NAME = "Best Buy Store Manager"
MENU_LINE = f"{(len(APP_NAME) + 16) * '-'}"
MENU_NUM_EXIT = '4'
EXIT_MSG = "Bye!"


def store_list_all_products(best_buy: store.Store) -> None:
    """
    Displays all products in the store's inventory.

    Iterates through the products in the given store and prints
    their details. If the inventory is empty, a message is shown.

    Args:
        best_buy (store.Store): The store instance to list products from.
    """
    if not best_buy.get_all_products():
        print("No products available.")
        return None
    print(MENU_LINE)
    for number, product in enumerate(best_buy.get_all_products(), 1):
        print(f"{number}. ", end="")
        product.show()
    print(MENU_LINE)
    return None


def store_show_total_amount(best_buy: store.Store) -> None:
    """
    Calculates and prints the total quantity of all products in the store.

    This function fetches the sum of all product quantities from the
    store's inventory and displays it framed by menu lines.

    Args:
        best_buy (store.Store): The store instance to calculate the total for.
    """
    total_items = best_buy.get_total_quantity()
    print(MENU_LINE)
    print(f"Total of {total_items} items in store.")
    print(MENU_LINE)


def store_make_order(best_buy: store.Store) -> None:
    """
    Handles the interactive process of creating and placing a customer order.

    This function manages the main order loop, coordinating product selection,
    quantity validation, and final order submission. It uses a temporary
    dictionary to consolidate quantities of the same product before processing.

    Args:
        best_buy (store.Store): The store instance where the order is placed.
    """
    if not best_buy.get_all_products():
        print("No products available.")
        return

    consolidated_basket = {}
    store_list_all_products(best_buy)

    while True:
        product = get_product(best_buy)
        if not product:
            break

        print(MENU_LINE)
        quantity = get_product_quantity(product)

        if quantity:
            _process_basket_item(consolidated_basket, product, quantity)
        else:
            print("Abort, product not added to order")

        print(MENU_LINE)

    if consolidated_basket:
        _finalize_store_order(best_buy, consolidated_basket)
    else:
        print("Abort, no product in order")


def _process_basket_item(basket: dict, product: products.Product, quantity: int) -> None:
    """
    Validates and adds a product to the temporary basket.

    Checks the combined quantity of the new request and existing basket items
    against the product's available stock and specific order limits (for
    LimitedProduct instances).

    Args:
        basket (dict): The current temporary order storage {Product: quantity}.
        product (products.Product): The product to be added.
        quantity (int): The quantity the user wants to add.
    """
    current_qty = basket.get(product, 0)
    total_intended_qty = current_qty + quantity

    if isinstance(product, products.LimitedProduct):
        if total_intended_qty > product.order_limit:
            print(f"Error: Maximum allowed for '{product.name}' is {product.order_limit}.")
            print(f"You already have {current_qty} in your basket.")
            return

    if not isinstance(product, products.NonStockedProduct):
        if total_intended_qty > product.quantity:
            print(f"Error: Not enough stock. Only {product.quantity} available in total.")
            return

    basket[product] = total_intended_qty
    print(f"Added {quantity}x '{product.name}' to your list!")


def _finalize_store_order(best_buy: store.Store, basket: dict) -> None:
    """
    Submits the consolidated order to the store and displays the result.

    Converts the internal basket dictionary into the format required by the
    Store's order method and handles potential execution errors.

    Args:
        best_buy (store.Store): The store instance to process the order.
        basket (dict): The validated and consolidated order data.
    """
    try:
        order_list = list(basket.items())
        total_payment = best_buy.order(order_list)

        print(MENU_LINE)
        print(f"Order made! Total payment: ${total_payment}\n")
    except ValueError as error:
        print(f"Order failed during processing: {error}")


def get_product(best_buy: store.Store) -> products.Product | None:
    """
    Prompts the user to select a product from the store by its list number.

    Validation is performed to ensure the input is a valid number within
     the inventory range. The user can terminate the selection process
     by entering 'F'.

    Args:
        best_buy (store.Store): The store instance to select products from.

    Returns:
        products.Product | None: The selected Product object, or None if the
                                 user finishes the selection.
    """
    product_list = best_buy.get_all_products()
    while True:
        print("Type 'F' to finish the order.")
        item_number = input("Which product # do you want to order? ")
        try:
            if item_number == 'F':
                return None
            if not item_number.isnumeric():
                raise ValueError(f"'{item_number}' must be a number "
                                 f"between 1 and {len(product_list)}")
            if int(item_number) not in range(1, len(product_list) + 1):
                raise ValueError(f"'{item_number}' is not a valid number "
                                 f"between 1 and {len(product_list)}")
            return product_list[int(item_number) - 1]
        except ValueError as error:
            print(error)


def get_product_quantity(product_to_check: products.Product) -> int | None:
    """
    Prompts the user to enter a valid purchase quantity for a specific product.

    Displays the product details and its available stock. Validates that the
    user input is a positive integer and does not exceed the current stock level.
    The user can cancel the selection for this specific item by entering '0'.

    Args:
        product_to_check (products.Product): The product object to verify stock for.

    Returns:
        int | None: The validated quantity to order, or None if the user
                    chooses to abort the selection.
    """
    print("- ", end="")
    product_to_check.show()
    product_quantity = product_to_check.quantity
    is_unlimited = isinstance(product_to_check, products.NonStockedProduct)

    while True:
        print("Type '0' to abort.")
        order_quantity = input("What amount do you want to order? ")
        try:
            if order_quantity == '0':
                return None
            if not order_quantity.isnumeric():
                raise ValueError(f"'{order_quantity}' must be a number.")

            val_quantity = int(order_quantity)

            if not is_unlimited and (val_quantity > product_quantity or val_quantity <= 0):
                raise ValueError(f"Not enough quantity, only {product_quantity} left.")
            elif is_unlimited and val_quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")

            return val_quantity
        except ValueError as error:
            print(error)


def exit_program(_best_buy: store.Store) -> None:
    """
    Displays the exit message to the user.

    This function is called by the menu dispatcher when the user
    selects the quit option.

    Args:
        _best_buy (store.Store): The store instance (unused in this function).
    """
    print(EXIT_MSG)


def show_menu() -> str:
    """
    Displays the main application menu to the user.

    Iterates through the MENU_DISPATCHER to print all available
    commands and their descriptions. After displaying the menu,
    it calls get_menu_choice() to handle user input.

    Returns:
        str: The validated menu choice entered by the user.
    """
    print(f"{7 * '+'} {APP_NAME} {7 * '+'}\n")
    for menu_number, menu_items in MENU_DISPATCHER.items():
        print(f"{menu_number}. - {menu_items['menu_text']}")
    print(MENU_LINE)
    return get_menu_choice()


def get_menu_choice() -> str:
    """
    Prompts the user for a menu selection and validates the input.

    The function continuously asks for input until a valid number
    corresponding to an entry in the MENU_DISPATCHER is provided.
    It handles non-numeric inputs and out-of-range numbers gracefully.

    Returns:
        str: A valid menu option key from the MENU_DISPATCHER.
    """
    while True:
        user_input = input("Enter a number: ")
        try:
            if not user_input.isnumeric():
                raise ValueError(f"'{user_input}' must be a number "
                                 f"between 1 and {len(MENU_DISPATCHER)}")
            if int(user_input) not in range(1, len(MENU_DISPATCHER) + 1):
                raise ValueError(f"'{user_input}' is not a valid number "
                                 f"between 1 and {len(MENU_DISPATCHER)}")
            return user_input
        except ValueError as error:
            print(error)


# Menu dispatcher:
MENU_DISPATCHER = {
    '1': {'cmd': store_list_all_products,
          'menu_text': "List all products in store"},
    '2': {'cmd': store_show_total_amount,
          'menu_text': "Show total amount in store"},
    '3': {'cmd': store_make_order,
          'menu_text': "Make an order"},
    '4': {'cmd': exit_program,
          'menu_text': "Quit"}
}


def start(best_buy: store.Store):
    """
    Runs the main application loop for the store manager.

    Continually displays the menu, executes the chosen command
    via the MENU_DISPATCHER, and checks for the exit condition.

    Args:
        best_buy (store.Store): The store instance to be managed
                                 throughout the session.
    """
    while True:
        menu_choice = show_menu()
        MENU_DISPATCHER[menu_choice]['cmd'](best_buy)
        if menu_choice == MENU_NUM_EXIT:
            break


def main():
    """
    Initializes the store with a default product inventory and assigns promotions.

    This setup demonstrates different product types (Standard, NonStocked, Limited)
    and applies various promotion strategies (Second Half Price, Third One Free,
    Percentage Discount) to showcase the store's pricing logic.
    """
    second_half_price = promotions.SecondHalfPrice("Second Half Price!")
    third_one_free = promotions.ThirdOneFree("3 for 2!")
    thirty_percent = promotions.PercentDiscount("30% Off!", discount_percent=30)

    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, order_limit=1)
    ]

    product_list[0].promotion = thirty_percent
    product_list[1].promotion = second_half_price
    product_list[2].promotion = third_one_free

    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == '__main__':
    main()
