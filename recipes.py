"""Модуль, содержащий классы для управления рецептами"""

class Ingredient:
    """Класс, описывающий один ингредиент блюда"""

    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.unit = unit
        self.quantity = quantity

    @property
    def quantity(self) -> float:
        """Геттер для получения количества ингредиента"""
        return self._quantity

    @quantity.setter
    def quantity(self, value: float) -> None:
        """Сеттер с валидацией: количество должно быть строго больше нуля"""
        parsed_value = float(value)
        if parsed_value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = parsed_value

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self) -> str:
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit
