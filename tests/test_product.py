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
    test_product = Product("Apple Neo", valid_price, 10)

    assert isinstance(test_product, Product)
    assert test_product.name == "Apple Neo"
    assert test_product.price == valid_price
    assert test_product.quantity == 10
    assert test_product.is_active() is True


def test_init_product_no_name():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Product("", 10.0, 5)


def test_init_product_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("Apple Neo", -1, 5)


def test_init_product_price_zero():
    test_product = Product("Apple Neo", 0, 111)
    assert isinstance(test_product, Product)


def test_init_product_negative_quantity():
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        Product("Apple Neo", 599, -5)


def test_init_product_quantity_zero():
    test_product = Product("Apple Neo", 599, 0)
    assert isinstance(test_product, Product)


@pytest.mark.parametrize("invalid_price_type",INVALID_PRICE_TYPES, ids=INVALID_PRICE_TYPES_IDS)
def test_init_product_price_invalid_types(invalid_price_type):
    with pytest.raises(TypeError, match="Price must be a number \(int or float\)"):
        Product("Apple Neo", invalid_price_type, 55)


@pytest.mark.parametrize("invalid_quantity", INVALID_QUANTITY_TYPES, ids=INVALID_QUANTITY_TYPES_IDS)
def test_init_product_quantity_invalid_types(invalid_quantity):
    with pytest.raises(TypeError, match="Quantity must be an integer"):
        Product("Apple Neo", 599, invalid_quantity)


def test_product_quantity_deactivate():
    test_product = Product("Apple Neo", 599, 10)
    test_product.quantity = 0
    assert not test_product.is_active()
    test_product = Product("Apple Neo", 599, 10)
    test_product.buy(10)
    assert not test_product.is_active()


def test_product_buy():
    test_product = Product("Apple Neo", 599, 10)
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


@pytest.mark.parametrize("invalid_price", INVALID_PRICE_TYPES, ids=INVALID_PRICE_TYPES_IDS)
def test_product_set_invalid_price(invalid_price):
    test_product = Product("Apple Neo", 599, 55)
    with pytest.raises(TypeError, match="Price must be a number \(int or float\)"):
        test_product.price = invalid_price


def test_non_stocked_product_quantity_immutable():
    test_product = NonStockedProduct("Apple Neo", 599)
    assert test_product.quantity == 0
    test_product.quantity = 100
    assert test_product.quantity == 0


def test_non_stocked_product_buy():
    test_product = NonStockedProduct("Apple Neo", 200)
    assert test_product.buy(3) == 600


def test_limited_product_order_limit():
    test_product = LimitedProduct("Apple Neo", 200, 10, 2)
    assert test_product.order_limit == 2


def test_limited_product_buy():
    test_product = LimitedProduct("Apple Neo", 200, 10, 2)
    assert test_product.buy(2) == 400


@pytest.mark.parametrize("order_limit", [3])
def test_limited_product_buy_over_limit(order_limit):
    test_product = LimitedProduct("Apple Neo", 200, order_limit, (order_limit - 1))
    with pytest.raises(ValueError, match=f"Quantity exceeds the order limit of {order_limit - 1}"):
        test_product.buy(order_limit)


def test_promotion_invalid_discount_type():
    with pytest.raises(TypeError, match="Discount percent must be an integer"):
        PercentDiscount("Sale", "10")


@pytest.mark.parametrize("discount_value", [-1, 101])
def test_promotion_invalid_discount_value(discount_value):
    with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
        PercentDiscount("Sale", discount_value)


def test_promotion_second_half_price():
    test_product = Product("Apple Neo", 100, 10)
    test_product.promotion = SecondHalfPrice("BOGO 50%")
    assert test_product.buy(2) == 150.0


def test_promotion_third_one_free():
    test_product = Product("Apple", 10, 10)
    test_product.promotion = ThirdOneFree("3 for 2")
    assert test_product.buy(3) == 20.0


def test_promotion_percent_discount():
    test_product = Product("Apple Neo", 100, 10)
    test_product.promotion = PercentDiscount("10% Off", 10)
    assert test_product.buy(5) == 450.0



