"""Модуль для тестирования классов управления рецептами"""
import pytest
from recipes import Ingredient, Recipe

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
