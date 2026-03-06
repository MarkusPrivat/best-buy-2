from abc import ABC, abstractmethod

class Promotion(ABC):
    def __init__(self, name: str, discount_percent: int =0):
        if not isinstance(name, str) and name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(discount_percent, int) and 0 <= discount_percent <= 100:
            raise ValueError("Discount percent must be an integer between 0 and 100")
        self.__name = name
        self.__discount_percent = discount_percent

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and name.strip():
            self.__name = name
        raise ValueError("Name must be a non-empty string")

    @property
    def discount_percent(self) -> float | int:
        return self.__discount_percent

    @discount_percent.setter
    def discount_percent(self, discount_percent: int):
        if isinstance(discount_percent, int) and 0 <= discount_percent <= 100:
            self.__discount_percent = discount_percent
        raise ValueError("Discount percent must be an integer between 0 and 100")

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        half = quantity // 2
        return (((quantity - half) * product.price)
                + product.price * .50 * half)


class ThirdOneFree(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        return product.price * (quantity - (quantity // 3))


class PercentDiscount(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        total = product.price * quantity
        discount = total * (self.discount_percent / 100)
        return total - discount
