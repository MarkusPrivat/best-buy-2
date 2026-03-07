"""
Unit tests for the product and promotion modules.

This module contains comprehensive pytest-based unit tests for the `products.py` module,
covering all product classes (`Product`, `NonStockedProduct`, `LimitedProduct`) and their
interaction with the promotion system (`PercentDiscount`, `SecondHalfPrice`, `ThirdOneFree`).

Test Coverage:
-------------
- **Product Initialization**: Valid and invalid constructor arguments.
- **Property Validation**: Type and value checks for name, price, and quantity.
- **Stock Management**: Automatic activation/deactivation based on quantity.
- **Purchase Logic**: Stock deduction, error cases, and promotion application.
- **Non-Stocked Products**: Special behavior for digital/non-inventory items.
- **Limited Products**: Order quantity restrictions and validation.
- **Promotion Calculations**: Correct discount application for all promotion types.

Test Cases:
-----------
### Product Class
- **Initialization**: Valid/invalid names, prices, and quantities.
- **Property Access**: Getters/setters for price and quantity.
- **Stock Behavior**: Automatic deactivation at zero quantity.
- **Purchase Validation**: Negative quantities, insufficient stock.

### NonStockedProduct Class
- **Quantity Immutability**: Always returns 0, ignores set attempts.
- **Purchase Logic**: No stock checks, promotion application.

### LimitedProduct Class
- **Order Limits**: Enforcement of maximum per-order quantities.
- **Purchase Validation**: Blocks orders exceeding the limit.

### Promotion Integration
- **PercentDiscount**: Correct percentage-based price reduction.
- **SecondHalfPrice**: "Buy one, get second at half price" logic.
- **ThirdOneFree**: "Buy two, get third free" logic.
- **Invalid Discounts**: Type and range validation for discount percentages.

Usage:
------
Run all tests with:
    pytest test_products.py -v

Run specific test groups with markers:
    pytest test_products.py::test_init_product -v
    pytest test_products.py::test_promotion_second_half_price -v
"""

import pytest


from products import Product, NonStockedProduct, LimitedProduct
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree


INVALID_PRICE_TYPES = ["Best Price", ["Best Price"], {"Best Price"}, {"Best Price": 599}]
INVALID_PRICE_TYPES_IDS= ["str", "list", "set", "dict"]
INVALID_QUANTITY_TYPES = [1.1, "Many", ["Big"], {"100"}, {"Best": 599}]
INVALID_QUANTITY_TYPES_IDS = ["float", "str", "list", "set", "dict"]

@pytest.mark.parametrize('valid_price',
                         [599, 599.99],
                         ids=["int_price", "float_price"])
def test_init_product(valid_price):
    """Verifies that a Product instance is initialized correctly with valid values."""
    test_product = Product("Apple Neo", valid_price, 10)

    assert isinstance(test_product, Product)
    assert test_product.name == "Apple Neo"
    assert test_product.price == valid_price
    assert test_product.quantity == 10
    assert test_product.is_active() is True


def test_init_product_no_name():
    """Ensures that creating a product with an empty name raises a ValueError."""
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Product("", 10.0, 5)


def test_init_product_negative_price():
    """Checks that a negative price raises a ValueError."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("Apple Neo", -1, 5)


def test_init_product_price_zero():
    """Validates that a price of 0 is accepted."""
    test_product = Product("Apple Neo", 0, 111)
    assert isinstance(test_product, Product)


def test_init_product_negative_quantity():
    """Checks that a negative quantity raises a ValueError."""
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        Product("Apple Neo", 599, -5)


def test_init_product_quantity_zero():
    """Validates that a quantity of 0 is accepted."""
    test_product = Product("Apple Neo", 599, 0)
    assert isinstance(test_product, Product)


@pytest.mark.parametrize("invalid_price_type",INVALID_PRICE_TYPES, ids=INVALID_PRICE_TYPES_IDS)
def test_init_product_price_invalid_types(invalid_price_type):
    """Checks that invalid price types raise a TypeError."""
    with pytest.raises(TypeError, match="Price must be a number \(int or float\)"):
        Product("Apple Neo", invalid_price_type, 55)


@pytest.mark.parametrize("invalid_quantity", INVALID_QUANTITY_TYPES, ids=INVALID_QUANTITY_TYPES_IDS)
def test_init_product_quantity_invalid_types(invalid_quantity):
    """Checks that invalid quantity types raise a TypeError."""
    with pytest.raises(TypeError, match="Quantity must be an integer"):
        Product("Apple Neo", 599, invalid_quantity)


def test_product_quantity_deactivate():
    """Verifies that the product deactivates automatically when quantity reaches 0."""
    test_product = Product("Apple Neo", 599, 10)
    test_product.quantity = 0
    assert not test_product.is_active()
    test_product = Product("Apple Neo", 599, 10)
    test_product.buy(10)
    assert not test_product.is_active()


def test_product_buy():
    """Checks that purchasing an item reduces the stock correctly."""
    test_product = Product("Apple Neo", 599, 10)
    test_product.buy(5)
    assert test_product.quantity == 5


def test_product_buy_to_many():
    """Ensures that buying more than the available stock raises a ValueError."""
    test_product = Product("Apple Neo", 599, 5)
    with pytest.raises(ValueError, match="Not enough stock available."):
        test_product.buy(6)


def test_product_buy_negative():
    """Ensures that purchasing a negative quantity raises a ValueError."""
    test_product = Product("Apple Neo", 599, 5)
    with pytest.raises(ValueError, match="Purchase quantity must be positive"):
        test_product.buy(-1)


def test_product_get_price():
    """Validates the product price getter."""
    test_product = Product("Apple Neo", 599, 5)
    assert test_product.price == 599


def test_product_set_price():
    """Validates the product price setter."""
    test_product = Product("Apple Neo", 599, 5)
    test_product.price = 500
    assert test_product.price == 500

def test_product_set_price_negativ():
    """Checks that setting a negative price raises a ValueError."""
    test_product = Product("Apple Neo", 599, 5)
    with pytest.raises(ValueError, match="Price cannot be negative"):
        test_product.price = -1


@pytest.mark.parametrize("invalid_price", INVALID_PRICE_TYPES, ids=INVALID_PRICE_TYPES_IDS)
def test_product_set_invalid_price(invalid_price):
    """Checks that setting an invalid price type raises a TypeError."""
    test_product = Product("Apple Neo", 599, 55)
    with pytest.raises(TypeError, match="Price must be a number \(int or float\)"):
        test_product.price = invalid_price


def test_non_stocked_product_quantity_immutable():
    """Verifies that the quantity for a NonStockedProduct remains 0."""
    test_product = NonStockedProduct("Apple Neo", 599)
    assert test_product.quantity == 0
    test_product.quantity = 100
    assert test_product.quantity == 0


def test_non_stocked_product_buy():
    """Checks the purchase logic for a NonStockedProduct."""
    test_product = NonStockedProduct("Apple Neo", 200)
    assert test_product.buy(3) == 600


def test_limited_product_order_limit():
    """Verifies that the order limit is set correctly for LimitedProduct."""
    test_product = LimitedProduct("Apple Neo", 200, 10, 2)
    assert test_product.order_limit == 2


def test_limited_product_buy():
    """Checks that a purchase within the order limit succeeds."""
    test_product = LimitedProduct("Apple Neo", 200, 10, 2)
    assert test_product.buy(2) == 400


@pytest.mark.parametrize("order_limit", [3])
def test_limited_product_buy_over_limit(order_limit):
    """Checks that a purchase exceeding the order limit raises a ValueError."""
    test_product = LimitedProduct("Apple Neo", 200, order_limit, (order_limit - 1))
    with pytest.raises(ValueError, match=f"Quantity exceeds the order limit of {order_limit - 1}"):
        test_product.buy(order_limit)


def test_promotion_invalid_discount_type():
    """Verifies that discount percent must be an integer."""
    with pytest.raises(TypeError, match="Discount percent must be an integer"):
        PercentDiscount("Sale", "10")


@pytest.mark.parametrize("discount_value", [-1, 101])
def test_promotion_invalid_discount_value(discount_value):
    """Verifies that discount percent must be between 0 and 100."""
    with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
        PercentDiscount("Sale", discount_value)


def test_promotion_second_half_price():
    """Validates the SecondHalfPrice promotion calculation."""
    test_product = Product("Apple Neo", 100, 10)
    test_product.promotion = SecondHalfPrice("BOGO 50%")
    assert test_product.buy(2) == 150.0


def test_promotion_third_one_free():
    """Validates the ThirdOneFree promotion calculation."""
    test_product = Product("Apple", 10, 10)
    test_product.promotion = ThirdOneFree("3 for 2")
    assert test_product.buy(3) == 20.0


def test_promotion_percent_discount():
    """Validates the percentage discount calculation."""
    test_product = Product("Apple Neo", 100, 10)
    test_product.promotion = PercentDiscount("10% Off", 10)
    assert test_product.buy(5) == 450.0
