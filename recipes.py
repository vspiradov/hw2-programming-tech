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

class Recipe:
    """Класс, представляющий рецепт блюда с набором ингредиентов"""

    def __init__(self, title: str, ingredients: list[Ingredient] | None = None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []

    def add_ingredient(self, ingredient: Ingredient) -> None:
        """
        Добавляет ингредиент в рецепт.
        Если ингредиент уже есть (совпадают имя и единица измерения),
        его количество суммируется
        """
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio: float | int) -> bool:
        """Возвращает True, если ratio положительное"""
        if type(ratio) not in (int, float):
            return False
        return ratio > 0

    def scale(self, ratio: float) -> 'Recipe':
        """Возвращает новый рецепт, пропорционально изменяя количество ингредиентов"""
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть положительным числом")
        
        scaled_ingredients = []
        for ing in self.ingredients:
            scaled_ing = Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            scaled_ingredients.append(scaled_ing) 
        return Recipe(self.title, scaled_ingredients)

    def __len__(self) -> int:
        """Возвращает количество уникальных ингредиентов в рецепте"""
        return len(self.ingredients)

    def __str__(self) -> str:
        """Возвращает название блюда и список ингредиентов в читаемом виде"""
        result = f"Рецепт: {self.title}\nИнгредиенты:\n"
        for ing in self.ingredients:
            result += f" - {ing}\n"
        return result.strip()
