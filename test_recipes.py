"""Модуль для тестирования классов управления рецептами"""
import pytest
from recipes import Ingredient, Recipe, ShoppingList

def test_ingredient_creation():
    """Проверка правильной инициализации атрибутов ингредиента"""
    ing = Ingredient("Мука", 500.0, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_quantity_nonnegative():
    """Проверка выброса исключения при отрицательном или нулевом количестве"""
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Мука", -10.0, "г")

def test_ingredient_str():
    """Проверка строкового представления ингредиента"""
    ing = Ingredient("Мука", 500.0, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    """Проверка равенства ингредиентов по имени и единице измерения"""
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 300.0, "г")
    ing3 = Ingredient("Сахар", 500.0, "г")
    ing4 = Ingredient("Мука", 500.0, "кг")
    # Совпадают имя и единица (количество не важно)
    assert ing1 == ing2
    # Разные имена
    assert ing1 != ing3
    # Разные единицы измерения
    assert ing1 != ing4

def test_recipe_creation():
    """Проверка правильной инициализации рецепта"""
    ing = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ing])
    assert recipe.title == "Пицца"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0] == ing

def test_recipe_add_ingredient():
    """Проверка добавления нового ингредиента и суммирования дубликатов"""
    recipe = Recipe("Пицца")
    ing1 = Ingredient("Мука", 300.0, "г")
    ing2 = Ingredient("Мука", 200.0, "г")
    ing3 = Ingredient("Сыр", 150.0, "г")
    recipe.add_ingredient(ing1)
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 300.0
    recipe.add_ingredient(ing2)
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 500.0
    recipe.add_ingredient(ing3)
    assert len(recipe) == 2

def test_recipe_scale():
    """Проверка масштабирования рецепта: создается новый объект, старый не меняется"""
    ing = Ingredient("Мука", 300.0, "г")
    recipe = Recipe("Пицца", [ing])
    scaled = recipe.scale(2.0)
    assert scaled is not recipe#два разных объекта?
    assert scaled.ingredients[0].quantity == 600.0#в новом кол-во изменилось?
    assert recipe.ingredients[0].quantity == 300.0#в старом не изменилось?
    with pytest.raises(ValueError, match="Коэффициент масштабирования должен быть положительным числом"):
        recipe.scale(-1.0)

def test_recipe_len():
    """Проверка подсчета уникальных ингредиентов через __len__"""
    recipe = Recipe("Пицца")
    assert len(recipe) == 0
    recipe.add_ingredient(Ingredient("Мука", 300.0, "г"))
    assert len(recipe) == 1
    recipe.add_ingredient(Ingredient("Мука", 200.0, "г"))#дубликат
    assert len(recipe) == 1
    recipe.add_ingredient(Ingredient("Сыр", 150.0, "г"))
    assert len(recipe) == 2

# В юнит-тестах проверяем внутреннее состояние объекта (_items)
def test_shopping_list_add_recipe():
    """Проверка добавления рецепта и масштабирования порций"""
    sl = ShoppingList()
    recipe = Recipe("Блины")
    recipe.add_ingredient(Ingredient("Мука", 200.0, "г"))
    sl.add_recipe(recipe, 2.0)
    assert len(sl._items) == 1
    assert sl._items[0][0].quantity == 400.0
    assert sl._items[0][1] == "Блины"
    with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
        sl.add_recipe(recipe, 0.0)

def test_shopping_list_remove_recipe():
    """Проверка удаления рецепта из списка покупок"""
    sl = ShoppingList()
    recipe1 = Recipe("Блины", [Ingredient("Мука", 200.0, "г")])
    recipe2 = Recipe("Омлет", [Ingredient("Яйцо", 2.0, "шт")])
    sl.add_recipe(recipe1, 1.0)
    sl.add_recipe(recipe2, 1.0)
    sl.remove_recipe("Блины")
    assert len(sl._items) == 1
    assert sl._items[0][1] == "Омлет"
    sl.remove_recipe("Пицца")
    assert len(sl._items) == 1

def test_shopping_list_get_list():
    """Проверка группировки, суммирования и сортировки списка покупок"""
    sl = ShoppingList()
    recipe1 = Recipe("Блины", [Ingredient("Мука", 200.0, "г"), Ingredient("Молоко", 500.0, "мл")])
    recipe2 = Recipe("Пирог", [Ingredient("Мука", 300.0, "г"), Ingredient("Яблоко", 3.0, "шт")])
    sl.add_recipe(recipe1, 1.0)
    sl.add_recipe(recipe2, 1.0)
    final_list = sl.get_list()
    assert len(final_list) == 3
    assert final_list[0].name == "Молоко"
    assert final_list[1].name == "Мука"
    assert final_list[2].name == "Яблоко"
    assert final_list[1].quantity == 500.0

def test_shopping_list_add_lists():
    """Проверка объединения двух списков покупок"""
    sl1 = ShoppingList()
    sl1.add_recipe(Recipe("Блины", [Ingredient("Мука", 200.0, "г")]), 1.0)
    sl2 = ShoppingList()
    sl2.add_recipe(Recipe("Омлет", [Ingredient("Яйцо", 2.0, "шт")]), 1.0)
    sl3 = sl1 + sl2
    assert isinstance(sl3, ShoppingList)
    assert len(sl3._items) == 2
    assert len(sl1._items) == 1
    assert len(sl2._items) == 1
