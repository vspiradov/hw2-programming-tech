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

class ShoppingList:
    """Класс для формирования списка покупок на основе рецептов"""

    def __init__(self):
        self._items: list[tuple[Ingredient, str]] = []

    def add_recipe(self, recipe: Recipe, portions: float) -> None:
        """Добавляет рецепт в список покупок с учетом количества порций"""
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, scaled_recipe.title))

    def remove_recipe(self, title: str) -> None:
        """Удаляет все ингредиенты указанного рецепта из списка покупок"""
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self) -> list[Ingredient]:
        """Возвращает итоговый список покупок, отсортированный по названию"""
        summary = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in summary:
                summary[key] += ingredient.quantity
            else:
                summary[key] = ingredient.quantity
        result = [Ingredient(name, quantity, unit) for (name, unit), quantity in summary.items()]
        result.sort(key=lambda x: x.name)
        return result

    def __add__(self, other: object) -> 'ShoppingList':
        """Объединяет два списка покупок в один новый список"""
        if not isinstance(other, ShoppingList):
            return NotImplemented
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list
