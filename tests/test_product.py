import pytest

import products
from products import Product



@pytest.mark.parametrize('valid_price',
                         [599, 599.99],
                         ids=["int_price", "float_price"])
def test_init_product(valid_price):
    test_product = products.Product("Apple Neo", valid_price, 10)

    assert isinstance(test_product, Product)
    assert test_product.name == "Apple Neo"
    assert test_product.price == valid_price
    assert test_product.quantity == 10
    assert test_product.active is True


def test_init_product_no_name():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Product("", 10.0, 5)


def test_init_product_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("Apple Neo", -1, 5)
    test_product = Product("Apple Neo", 0, 111)
    assert isinstance(test_product, Product)


def test_init_product_negative_quantity():
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        Product("Apple Neo", 599, -5)
    test_product = Product("Apple Neo", 599, 0)
    assert isinstance(test_product, Product)


@pytest.mark.parametrize("invalid_price", [
    "Best Price",
    ["Best Price"],
    {"Best Price"},
    {"Best Price": 599}
], ids=[
    "str",
    "list",
    "set",
    "dict"
])
def test_init_product_price_invalid_types(invalid_price):
    with pytest.raises(TypeError, match="Price must be a number \(int or float\)"):
        Product("Apple Neo", invalid_price, 55)


@pytest.mark.parametrize("invalid_quantity", [
    1.1,
    "Many",
    ["Big"],
    {"100"},
    {"Best": 599}
], ids=[
    "float",
    "str",
    "list",
    "set",
    "dict"
])
def test_init_product_quantity_invalid_types(invalid_quantity):
    with pytest.raises(TypeError, match="Quantity must be an integer"):
        Product("Apple Neo", 599, invalid_quantity)


def test_product_quantity_deactivate():
    test_product = products.Product("Apple Neo", 599, 10)
    test_product.set_quantity(0)
    assert test_product.is_active() == False
    test_product = products.Product("Apple Neo", 599, 10)
    test_product.buy(10)
    assert test_product.is_active() == False


def test_product_buy():
    test_product = products.Product("Apple Neo", 599, 10)
    test_product.buy(5)
    assert test_product.quantity == 5


def test_product_buy_to_many():
    test_product = Product("Apple Neo", 599, 5)
    with pytest.raises(ValueError, match="Not enough stock available."):
        test_product.buy(6)


def test_product_buy_negative():
    test_product = Product("Apple Neo", 599, 5)
    with pytest.raises(ValueError, match="Purchase quantity must be positive"):
        test_product.buy(-1)


def test_product_get_price():
    test_product = Product("Apple Neo", 599, 5)
    assert test_product.price == 599


def test_product_set_price():
    test_product = Product("Apple Neo", 599, 5)
    test_product.price = 500
    assert test_product.price == 500

def test_product_set_price_negativ():
    test_product = Product("Apple Neo", 599, 5)
    with pytest.raises(ValueError, match="Price cannot be negative"):
        test_product.price = -1


@pytest.mark.parametrize("invalid_price", [
    "Best Price",
    ["Best Price"],
    {"Best Price"},
    {"Best Price": 599}
], ids=[
    "str",
    "list",
    "set",
    "dict"
])
def test_product_set_price(invalid_price):
    test_product = Product("Apple Neo", 599, 55)
    with pytest.raises(TypeError, match="Price must be a number \(int or float\)"):
        test_product.price = invalid_price
